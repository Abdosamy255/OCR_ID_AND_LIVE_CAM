#import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pytesseract
import sys

#pip install pytesseract
camera = None
ocr_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = ocr_path

def extract_text_from_image(image):
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

def cleanup():
    global camera
    if camera is not None and camera.isOpened():
        camera.release()
        cv2.destroyAllWindows()
        print("Camera released.")
    sys.exit(0)




def main():
    global camera
    print("Attempting to start camera...")
    
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("cv2.CAP_DSHOW Failed.")
        camera = cv2.VideoCapture(0)
        
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    #set camera properties
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)
    
    print("Camera started successfully.")
    print("Press 'c' to capture an image and extract text.")
    print("Press 'q' to quit.")
    
    try:    
        while True:
            ret, frame = camera.read()
            
            if not ret:
                print("Error: Could not read frame.")
                break
            
            cv2.imshow("Camera Feed - Press 'q' to quit", frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('c'):
                print("capturing image...")
                extracted_text = extract_text_from_image(frame)
                if extracted_text.strip():
                    print("Extracted Text:")
                    print(extracted_text)
                
                else:
                    print('No text captured.')
                    
            elif key == ord('q'):
                print("Quitting...")
                break
    finally:        
        cleanup()
    
if __name__ == "__main__":
    main()