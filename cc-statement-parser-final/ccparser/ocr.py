from typing import List
try:
    import pytesseract
except Exception:
    pytesseract = None

def ocr_images(pages):
    if pytesseract is None:
        return []
    out = []
    for p in pages:
        try:
            im = p.to_image(resolution=300).original
            text = pytesseract.image_to_string(im)
            out.append(text or '')
        except Exception:
            out.append('')
    return out
