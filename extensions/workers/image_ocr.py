import pytesseract
from PIL import Image

def extract_text(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return f"📄 OCR Text:\n{text.strip()}"
    except Exception as e:
        return f"⚠️ OCR Error: {e}"
