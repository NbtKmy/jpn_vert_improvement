import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse


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

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Pre-process for OCR')
    parser.add_argument('input', help='Name of original image')
    parser.add_argument('output', help='Name of output image')
    args = parser.parse_args() 


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
    cv2.imwrite(args.output, res)

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
    cv2.imwrite('resultWstencil.jpg', newImg)

    # Textbox ausschneiden mit np (box = image[y:y+h, x:x+w])
    # line_num = 0
    # for c in line_conts:
        # line = grau_img[c[1]:c[1]+c[3], c[0]:c[0]+c[2]]
        # n, bi_line = binarize(line)
        # cv2.imwrite('line_{}.tif'.format(line_num), bi_line)
        # line_num += 1


