import os
import pytesseract
from PIL import Image
import time

OUTPUT_DIR = "/app/data/image_analysis"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_image(image_path: str) -> str:
    """Extract text from image using OCR"""
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        report = f"[OCR Extracted from {os.path.basename(image_path)}]:\n{text}"
        # Save extracted text
        with open(os.path.join(OUTPUT_DIR, f"ocr_{int(time.time())}.txt"), "w") as f:
            f.write(report)
        print(f"✅ OCR processed {image_path}")
        return report
    except Exception as e:
        return f"⚠️ OCR failed: {e}"
