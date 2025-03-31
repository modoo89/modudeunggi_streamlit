
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_kb_price_from_kbland_selenium(keyword):
    options = Options()
    options.add_argument("--headless")  # 백그라운드에서 실행 (UI 안보임)
    driver = webdriver.Chrome(options=options)

    try:
        # KBland 사이트 접속
        driver.get(f'https://kbland.kr/search?query={keyword}')
        time.sleep(3)

        # 첫 번째 검색 결과 클릭
        first_result = driver.find_element(By.CSS_SELECTOR, ".result-box .title a")
        first_result.click()
        time.sleep(3)

        # 시세/실거래가 탭 클릭
        tab = driver.find_element(By.LINK_TEXT, "시세")
        tab.click()
        time.sleep(2)

        # 최신 기준일의 시세 정보 추출
        price_element = driver.find_element(By.CSS_SELECTOR, ".price-box .price p:nth-child(1)")
        price_text = price_element.text.strip().replace(",", "").replace("억", "0000").replace("만", "")

        if price_text.isdigit():
            return int(price_text) * 10000  # 원 단위로 변환
        else:
            return "❌ 시세 정보 추출 실패"
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}"
    finally:
        driver.quit()
