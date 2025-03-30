
import requests
from bs4 import BeautifulSoup
import re

def get_kb_price_from_kbland(address: str, area: float):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://kbland.kr/search?query={address}"
    res = requests.get(search_url, headers=headers)
    if res.status_code != 200:
        return "❌ KB 시세 검색 오류"

    soup = BeautifulSoup(res.text, "html.parser")
    link_tag = soup.find("a", href=True)
    if not link_tag:
        return "❌ 검색 결과 없음"

    detail_url = "https://kbland.kr" + link_tag["href"]
    detail_res = requests.get(detail_url, headers=headers)
    if detail_res.status_code != 200:
        return "❌ 상세 페이지 오류"

    detail_soup = BeautifulSoup(detail_res.text, "html.parser")
    table = detail_soup.find("table")
    if not table:
        return "❌ 시세 테이블 없음"

    price_dict = {}
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            try:
                m2 = float(re.search(r"\d+\.\d+", cols[0].text).group())
                price_text = cols[1].text.strip()
                price = int(re.sub(r"[^\d]", "", price_text)) * 10000
                price_dict[m2] = price
            except:
                continue

    if not price_dict:
        return "❌ 면적별 시세 없음"

    closest = min(price_dict.keys(), key=lambda x: abs(x - area))
    return price_dict[closest]
