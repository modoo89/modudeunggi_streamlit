
import streamlit as st
from modules.extract import extract_address_and_area_from_pdf
from modules.kbland import get_kb_price_from_kbland
from modules.loan_calc import calc_loan_by_11_conditions
from modules.report import create_pdf_report
import tempfile
import os

st.set_page_config(page_title="모두등기 대출 리포트", layout="centered")
st.title("📄 모두등기 대출 리포트 자동 생성기")

uploaded_file = st.file_uploader("등기부등본 PDF를 업로드하세요", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    st.success("✅ PDF 업로드 완료")

    parsed = extract_address_and_area_from_pdf(pdf_path)
    address = parsed["주소"]
    area = parsed["전용면적"]

    st.write(f"📍 **주소**: {address}")
    st.write(f"📐 **전용면적**: {area}㎡")

    apt_name = address.split()[-1]  # 주소에서 아파트 이름 유추
    dong = address.split()[-2]

    price = get_kb_price_from_kbland(apt_name, dong, area)
    if isinstance(price, str):
        st.error(price)
    else:
        st.write(f"📈 **KB 시세**: {price:,} 원")
        results = calc_loan_by_11_conditions(price)
        st.dataframe(results)

        report_path = os.path.join(tempfile.gettempdir(), "modudeunggi_report.pdf")
        create_pdf_report(address, area, price, results, save_path=report_path)

        with open(report_path, "rb") as f:
            st.download_button("📥 리포트 PDF 다운로드", f.read(), file_name="modudeunggi_report.pdf")
