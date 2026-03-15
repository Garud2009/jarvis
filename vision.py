import pytesseract, os # type: ignore
from PIL import ImageGrab, ImageOps # optic toolset

t_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # binary path
if os.path.exists(t_path): pytesseract.pytesseract.tesseract_cmd = t_path # link node

def read_screen(): # optic sensor
    if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        return "OCR engine missing, Sir." # node blackout
    try:
        img = ImageGrab.grab() # capture light
        img = ImageOps.autocontrast(img.convert('L')) # normalize data
        txt = pytesseract.image_to_string(img).strip() # scan patterns
        return txt if txt else "Visual field is clear, Sir." # res sync
    except Exception as e:
        print(f"Vision Error: {e}") # internal log
        return "Optic node glitch, Sir." # hardware fail
