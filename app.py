
import streamlit as st
from modules.naver_kb_selenium import get_kb_price_from_naver_selenium
from modules.kbland_kb_selenium import get_kb_price_from_kbland_selenium

def main():
    st.title("모두등기 대출 리포트")
    
    # 주소 입력
    keyword = st.text_input("주소를 입력하세요 (예: 청담동 108 건영아파트)")
    
    if keyword:
        # 네이버 부동산에서 KB 시세 조회
        price_naver = get_kb_price_from_naver_selenium(keyword)
        st.write("네이버 부동산 시세:", price_naver)

        # KBland에서 KB 시세 조회
        price_kbland = get_kb_price_from_kbland_selenium(keyword)
        st.write("KBland 시세:", price_kbland)

        # 시세 비교 리포트 생성
        if isinstance(price_naver, int) and isinstance(price_kbland, int):
            st.write(f"네이버 부동산과 KBland 시세가 일치하는 경우, 선택하여 리포트에 반영할 수 있습니다.")
        else:
            st.write("시세를 직접 입력해주세요.")
            manual_price = st.number_input("KB 시세 (원 단위)", min_value=1000, step=100)
            st.write(f"입력된 KB 시세: {manual_price:,} 원")
    
if __name__ == "__main__":
    main()
