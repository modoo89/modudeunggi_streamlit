
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_kb_price_from_naver_selenium(keyword):
    options = Options()
    options.add_argument("--headless")  # 백그라운드에서 실행 (UI 안보임)
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://land.naver.com")
        time.sleep(2)

        # 검색창에 주소 입력하고 검색
        search_box = driver.find_element(By.ID, "queryInputHeader")
        search_box.send_keys(keyword)
        search_box.submit()
        time.sleep(2)

        # 첫 번째 검색 결과 클릭
        first_result = driver.find_element(By.CSS_SELECTOR, ".search_result_list li a")
        first_result.click()
        time.sleep(2)

        # '시세/실거래가' 탭 클릭
        tab = driver.find_element(By.LINK_TEXT, "시세/실거래가")
        tab.click()
        time.sleep(2)

        # 최신 기준일의 일반평균가 추출
        avg_price = driver.find_element(By.CSS_SELECTOR, ".tbl_price tbody tr:first-child td:nth-child(2)")
        price_text = avg_price.text.strip().replace(",", "").replace("억", "0000").replace("만", "")

        if price_text.isdigit():
            return int(price_text) * 10000  # 원 단위로 변환
        else:
            return "❌ 시세 정보 추출 실패"
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}"
    finally:
        driver.quit()
