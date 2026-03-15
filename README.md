# ID OCR Scanner

A professional Streamlit app for extracting structured data from ID card images using OpenCV preprocessing and Tesseract OCR.

## Features

- Modern Streamlit UI with a clean layout
- Automatic image preprocessing for better OCR quality
- OCR language support (`eng`, `ara+eng`)
- Smart parsing for common fields:
  - Name
  - Organization
  - ID number
  - Phone
  - Email
  - Dates
- Export results as JSON and TXT

## Project Files

- `app.py`: Main Streamlit application (recommended entrypoint)
- `app_with_Enhanced.py`: Alternative enhanced UI variant
- `App_live.py`: OpenCV live camera OCR script

## Requirements

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

### Windows Tesseract

Install Tesseract and make sure one of these is true:

1. `tesseract` is available in your system PATH, or
2. It exists at `C:\Program Files\Tesseract-OCR\tesseract.exe`, or
3. You provide `TESSERACT_CMD` via Streamlit secrets.

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Notes

- OCR quality depends heavily on image sharpness and lighting.
- For best results, use high-resolution images and keep text horizontal.
