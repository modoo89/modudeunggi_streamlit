
from fpdf import FPDF
import datetime

def create_pdf_report(address, area, price, results, save_path="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", "", uni=True)
    pdf.set_font("Arial", "", 12)
    pdf.set_font_size(16)
    pdf.cell(0, 10, "모두등기 대출 리포트", ln=True)
    pdf.ln(5)
    pdf.set_font_size(12)
    pdf.cell(0, 10, f"📍 주소: {address}", ln=True)
    pdf.cell(0, 10, f"📐 전용면적: {area:.2f}㎡", ln=True)
    pdf.cell(0, 10, f"📈 KB 시세: {price:,} 원", ln=True)
    pdf.cell(0, 10, f"📅 생성일: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(10)
    pdf.cell(60, 10, "조건", 1)
    pdf.cell(35, 10, "LTV금액", 1)
    pdf.cell(20, 10, "DSR", 1)
    pdf.cell(20, 10, "금리", 1)
    pdf.cell(30, 10, "월상환금", 1)
    pdf.cell(30, 10, "필요소득", 1, ln=True)
    for r in results:
        pdf.cell(60, 10, r["조건"], 1)
        pdf.cell(35, 10, r["LTV금액"], 1)
        pdf.cell(20, 10, r["DSR"], 1)
        pdf.cell(20, 10, r["금리"], 1)
        pdf.cell(30, 10, r["월상환금"], 1)
        pdf.cell(30, 10, r["필요소득"], 1, ln=True)
    pdf.output(save_path)
