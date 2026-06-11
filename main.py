import requests
import schedule
import time
import json
import os
from datetime import date

TOKEN = "8662302479:AAGoR8ZMMvzl0bzO_Ui-3-Gj0pfpBzUewQs"
CHANNEL = "@demokenh"
FILE_LICH_SU = "/tmp/lich_su.json"
API_KEY = "604ff024a67112ee99258e7e258c3348"

GIAI_DAU = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": 39,
    "🇪🇸 La Liga": 140,
    "🇩🇪 Bundesliga": 78,
    "🇮🇹 Serie A": 135,
    "🇫🇷 Ligue 1": 61,
    "🏆 Champions League": 2,
    "🌍 World Cup": 1,
    "🤝 Giao Hữu": 5,
}

def doc_lich_su():
    try:
        with open(FILE_LICH_SU, "r") as f:
            return json.load(f)
    except:
        return []

def luu_lich_su(da_gui):
    with open(FILE_LICH_SU, "w") as f:
        json.dump(da_gui, f)

def gui_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def lay_ket_qua(league_id):
    hom_nay = date.today().strftime("%Y-%m-%d")
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "league": league_id,
        "date": hom_nay,
        "season": 2026
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data.get("response", [])

def kiem_tra_va_gui():
    print("⏳ Đang kiểm tra kết quả mới...")
    da_gui = doc_lich_su()

    for ten_giai, league_id in GIAI_DAU.items():
        fixtures = lay_ket_qua(league_id)
        if not fixtures:
            continue

        tin = f"*{ten_giai}*\n\n"
        co_moi = False

        for match in fixtures:
            fixture_id = str(match["fixture"]["id"])
            status = match["fixture"]["status"]["short"]
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            score_home = match["goals"]["home"]
            score_away = match["goals"]["away"]
            time_match = match["fixture"]["date"][11:16]

            if fixture_id in da_gui:
                continue
            if status not in ["FT", "AET", "PEN"]:
                continue

            tin += f"🕐 {time_match}\n"
            tin += f"🏟 {home} {score_home} - {score_away} {away}\n"
            tin += "➖➖➖➖➖➖\n"
            da_gui.append(fixture_id)
            co_moi = True

        if co_moi:
            gui_telegram(tin)
            print(f"✅ Gửi mới: {ten_giai}")

    luu_lich_su(da_gui)
    print("✔ Kiểm tra xong!\n")

kiem_tra_va_gui()

schedule.every(5).minutes.do(kiem_tra_va_gui)

print("🤖 Bot đang chạy 24/24...")
while True:
    schedule.run_pending()
    time.sleep(60)
