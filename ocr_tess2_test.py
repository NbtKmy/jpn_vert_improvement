import pyocr
import pyocr.builders
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

import sys
import argparse

# Für Vorarbeitung

# Gaussian Filer (x & y sind Kernel-Size)
def gaussianFilter(img1, x, y):
    size = (x, y)
    gaublur = cv2.GaussianBlur(img1, size, 0)
    return gaublur

# Laplacian Filter
def lapcalian(img2):
    lap = cv2.Laplacian(img2, cv2.CV_8UC1)
    return lap

# MedianFilter (a = kernel size, muss eine ungerade Zahl sein)
def medianFilter(img3, a):
    medBlur = cv2.medianBlur(img3, a)
    return medBlur

# Morphology (hier Closing-Verfahren = zuerst Dilation dann danach Erosion; b & c sind für die Kernel-Size)
def morph(img4, b, c):
    kernel = np.ones((b, c), np.uint8)
    dilation = cv2.dilate(img4, kernel, iterations = 1)
    erosion = cv2.erode(dilation, kernel, iterations = 1)
    return erosion

# Binarisierung hier nur Otsu
def binarize(img5):
    ret, th = cv2.threshold(img5, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return ret, th

# Textbox erstellen
def getTextbox(img6, original_img):
    contours, hierarchy = cv2.findContours(img6, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = original_img.shape[0] * original_img.shape[1] * 1e-4
    tmp = original_img.copy()
    conts = []
    line_conts = []
    if len(contours) > 0:
        for i, contour in enumerate(contours):
            rect = cv2.boundingRect(contour)
            if rect[2] < 10 or rect[3] < 10:
                continue
            area = cv2.contourArea(contour)
            if area < min_area:
                continue
            # rect[0] = x, rect[1] = y, rect[2] = w, rect[3] = h
            cv2.rectangle(tmp, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 0), 2)
            box = np.array([[rect[0], rect[1]], [rect[0]+rect[2], rect[1]], [rect[0]+rect[2], rect[1]+rect[3]], [rect[0], rect[1]+rect[3]]])
            conts.append(box)
            line_box = [rect[0], rect[1], rect[2], rect[3]]
            line_conts.append(line_box)
        return tmp, conts, line_conts



# Für OCR

def ocr(img_path, output, lng):
    # Getting ocr tool
    tools = pyocr.get_available_tools()

    if len(tools) == 0:
        print("No OCR software found")
        sys.exit(1)
 
    # Ocr[0] = tesseract
    tool = tools[0]
    
    img1 = Image.open(img_path)
    # Getting text from image
	# jpn_vert2 muss noch einmal trainiert werden - wegen der Fehlermeldung 'Failed to load any lstm-specific dictionaries for lang jpn_vert2!!'
	# siehe https://github.com/tesseract-ocr/tesstrain/issues/28 - dennoch funtioniert über command line
    res = tool.image_to_string(img1, lang=lng, builder=pyocr.builders.LineBoxBuilder(tesseract_layout=5))
        
    
    # Output als Textdatei
    # with open('./results/last_result/res_bsp1_2.txt', mode='w') as f:
    #    f.write(res)

    img = cv2.imread(img_path)
    #out = cv2.imread(args.input)
    orgHeight, orgWidth = img.shape[0], img.shape[1]
    size = (orgWidth//2, orgHeight//2)
 
    for d in res:
        print(d.content) # which character is recognized?
        ##print(d.position) # which area are targeted?
        cv2.rectangle(img, d.position[0], d.position[1], (0, 0, 255), 2) # create red boxes for the recognized areas
 
    # Show the image with boxes
    img_resize = cv2.resize(img, size) 
    cv2.imwrite(args.output, img_resize)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OCR process')
    parser.add_argument('input', help='Name and path of the original image')
    parser.add_argument('output', help='Name of output image')
    parser.add_argument('lang', help='Name of the language for OCR')
    args = parser.parse_args() 

    # Vorarbeitung
    img = cv2.imread(args.input)
    h, s, grau_img = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))

    schritt1 = gaussianFilter(grau_img, 5, 5)
    schritt2 = lapcalian(schritt1)
    ret, schritt3 = binarize(schritt2)

    # Morph-closing
    kernel = np.ones((120, 5), np.uint8)
    closing = cv2.morphologyEx(schritt3, cv2.MORPH_CLOSE, kernel)

    schritt4 = morph(closing, 50, 3)
    schritt5 = lapcalian(schritt4)
    res, conts, line_conts = getTextbox(schritt5, img)


    # output result image with boxes
    #cv2.imwrite(args.output, res)

    # Textline im Image werden nur zugelassen. Sonstige Elemente werden gedeckt
    # mit Grau füllen 
    # stencil = np.tile(np.uint8([127]), img.shape)

    # Mit Schwarz füllen
    stencil = np.zeros(img.shape).astype(img.dtype)

    # Für floodFill
    h, w = img.shape[:2]
    mask = np.zeros((h + 2, w + 2), dtype=np.uint8)

    color = [255, 255, 255]
    cv2.fillPoly(stencil, conts, color)
    filledImg = cv2.bitwise_and(img, stencil)
    retval, newImg, mask, rect = cv2.floodFill(
    filledImg,
    mask,
    seedPoint=(0, 0),
    newVal=(255, 255, 255),
    loDiff=(20, 20, 20),
    upDiff=(20, 20, 20),
    flags=4 | 255 << 8,
    )
    
    # OCR-Prozess
    ocr(newImg, args.output, args.lang)
