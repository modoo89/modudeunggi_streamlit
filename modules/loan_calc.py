
def calc_monthly_payment(principal: int, annual_rate: float, years: int = 40) -> int:
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        return principal // n
    return int(principal * r * (1 + r) ** n / ((1 + r) ** n - 1))

def calc_loan_by_11_conditions(price: int) -> list:
    방공제 = 55_000_000
    conditions = [
        {"설명": "은행(비규제/1주택)", "LTV": 0.70, "금리": 4.2, "DSR": "40%", "소득나누기": 7},
        {"설명": "은행(비규제/다주택)", "LTV": 0.60, "금리": 4.2, "DSR": "40%", "소득나누기": 7},
        {"설명": "보험사(비규제/1주택)", "LTV": 0.70, "금리": 4.5, "DSR": "50%", "소득나누기": 8},
        {"설명": "보험사(비규제/다주택)", "LTV": 0.60, "금리": 4.5, "DSR": "50%", "소득나누기": 8},
        {"설명": "은행(규제/1주택)", "LTV": 0.50, "금리": 4.2, "DSR": "40%", "소득나누기": 7},
        {"설명": "은행(규제/다주택)", "LTV": 0.40, "금리": 4.2, "DSR": "40%", "소득나누기": 7},
        {"설명": "보험사(규제/1주택)", "LTV": 0.50, "금리": 4.5, "DSR": "50%", "소득나누기": 8},
        {"설명": "보험사(규제/다주택)", "LTV": 0.40, "금리": 4.5, "DSR": "50%", "소득나누기": 8},
        {"설명": "은행&보험사(규제/다주택매수)", "LTV": 0.30, "금리": 4.2, "DSR": "-", "소득나누기": None},
        {"설명": "상호금융(선순위)", "LTV": 0.85, "금리": 5.3, "방공제": True, "DSR": "X"},
        {"설명": "상호금융(후순위)", "LTV": 0.80, "금리": 5.3, "방공제": True, "DSR": "X"},
    ]
    results = []
    for cond in conditions:
        raw_loan = int(price * cond["LTV"])
        loan = raw_loan - 방공제 if cond.get("방공제") else raw_loan
        loan = max(0, loan)
        monthly_payment = int(loan * (cond["금리"] / 100) / 12) if cond["설명"].startswith("상호금융") else calc_monthly_payment(loan, cond["금리"], 40)
        income = int(loan / cond["소득나누기"]) if cond.get("소득나누기") else None
        results.append({
            "조건": cond["설명"],
            "LTV금액": f"{loan:,}원",
            "DSR": cond["DSR"],
            "금리": f"{cond['금리']}%",
            "월상환금": f"{monthly_payment:,}원",
            "필요소득": f"{income:,}원" if income else "-"
        })
    return results
