
import fitz
import re

def extract_address_and_area_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    address_match = re.search(r'(서울|경기|인천|부산|대구|대전|광주|울산|세종)[^\n]+?(동|읍|면)[^\n]+?[0-9\-]+호?', text)
    address = address_match.group(0).strip() if address_match else "❌ 주소 미추출"
    area_match = re.search(r'([0-9]+\.[0-9]+)\s?㎡', text)
    area = float(area_match.group(1)) if area_match else 0.0
    return {"주소": address, "전용면적": area}
