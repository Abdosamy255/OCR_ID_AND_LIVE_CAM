import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pytesseract

#pip install pytesseract

ocr_path =r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = ocr_path


def extract_text_from_id(image):
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text


st.title("ID Scanner with OCR")
st.write("Upload an ID card image to extract INFO using OCR.")





uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    st.image(image, caption='Uploaded ID.')
    
    extracted_text = extract_text_from_id(image_np)
    st.subheader("Extracted Text:")
    text_list = extracted_text.splitlines()
    Organization_Name = text_list[0]+ ' '+text_list[1]
    Employee_Name = text_list[8]
    phobe_number = text_list[6]
    
    st.write('Organization Name:',text_list[0],' ',text_list[1])
    st.write('Employee Name:',text_list[8])
    st.write(text_list[3])
    st.write(text_list[4])
    st.write(text_list[5])
    st.write(text_list[6])
    
    
    
    
    #['THYNK', 'UNLIMITED', '', 'ldcard 123-456-7890', 
    # 'Email: helo@eallygreatstecom', '‘Address <123 Anywhere. Any City',
    # 'Phone: +123-456-7890', '', 'Benjamin Shah', '', 'tive Director', '']