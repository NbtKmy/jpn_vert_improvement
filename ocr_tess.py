import pyocr
import pyocr.builders
from PIL import Image
import cv2
import sys
import argparse


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

    
    # OCR-Prozess
    ocr(args.input, args.output, args.lang)
