
import requests
from bs4 import BeautifulSoup
import re

def get_kb_price_from_kbland(apt_name, dong, area):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Step 1: 단지명으로 검색
    search_url = f"https://kbland.kr/search?query={apt_name}"
    res = requests.get(search_url, headers=headers)
    if res.status_code != 200:
        return "❌ KB 검색 오류"

    soup = BeautifulSoup(res.text, "html.parser")

    # Step 2: 검색 결과 중 첫 번째 아파트 링크 가져오기
    link_tag = soup.find("a", href=re.compile(r"aptDetail\?aptCode=\d+"))
    if not link_tag:
        return "❌ 단지 검색 실패"

    detail_url = "https://kbland.kr" + link_tag['href']
    detail_res = requests.get(detail_url, headers=headers)
    if detail_res.status_code != 200:
        return "❌ 단지 상세페이지 오류"

    detail_soup = BeautifulSoup(detail_res.text, "html.parser")

    # Step 3: 면적별 매매 시세 찾기
    rows = detail_soup.find_all("tr")
    price_dict = {}

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            try:
                area_text = cols[0].text.strip()
                price_text = cols[1].text.strip()

                m2_match = re.search(r"\d+\.\d+", area_text)
                if not m2_match:
                    continue
                m2 = float(m2_match.group())
                price_num = int(re.sub(r"[^\d]", "", price_text)) * 10000
                price_dict[m2] = price_num
            except:
                continue

    # Step 4: 가장 가까운 면적의 시세 선택
    if not price_dict:
        return "❌ 시세 정보 없음"

    closest = min(price_dict.keys(), key=lambda x: abs(x - area))
    return price_dict[closest]
