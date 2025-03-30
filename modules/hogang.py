
import requests
from bs4 import BeautifulSoup
import re

def get_kb_price_from_hogang(address, area):
    apt_keyword = re.sub(r"[0-9\-]+호?", "", address.split()[-1])
    search_url = f"https://hogangnono.com/search/{apt_keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    if res.status_code != 200:
        return "❌ 호갱노노 접속 오류"
    soup = BeautifulSoup(res.text, "html.parser")
    link_tag = soup.find("a", href=re.compile(r"apt/\d+"))
    if not link_tag:
        return "❌ 아파트 검색 실패"
    apt_url = "https://hogangnono.com" + link_tag['href']
    apt_page = requests.get(apt_url, headers=headers)
    if apt_page.status_code != 200:
        return "❌ 아파트 상세페이지 오류"
    soup = BeautifulSoup(apt_page.text, "html.parser")
    price_blocks = soup.find_all("div", class_="PriceGraph_graph__tG1Gh")
    price_dict = {}
    for graph in price_blocks:
        title = graph.find("div", class_="PriceGraph_area__B9LCg")
        price = graph.find("div", class_="PriceGraph_price__p6A1M")
        if title and price:
            try:
                m2 = float(re.search(r"\d+\.\d+", title.text).group())
                price_num = int(re.sub(r"[^\d]", "", price.text)) * 10000
                price_dict[m2] = price_num
            except:
                continue
    closest = min(price_dict.keys(), key=lambda x: abs(x - area)) if price_dict else None
    return price_dict[closest] if closest else "❌ 면적에 맞는 시세 없음"
