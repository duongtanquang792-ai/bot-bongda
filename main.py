import requests
import schedule
import time
import json
import os

TOKEN = "8662302479:AAGoR8ZMMvzl0bzO_Ui-3-Gj0pfpBzUewQs"
CHANNEL = "@demokenh"
FILE_LICH_SU = "lich_su.json"

GIAI_DAU = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": 4328,
    "🇪🇸 La Liga": 4335,
    "🇩🇪 Bundesliga": 4331,
    "🇮🇹 Serie A": 4332,
    "🇫🇷 Ligue 1": 4334,
    "🏆 Champions League": 4480,
}

def doc_lich_su():
    if os.path.exists(FILE_LICH_SU):
        with open(FILE_LICH_SU, "r") as f:
            return json.load(f)
    return []

def luu_lich_su(da_gui):
    with open(FILE_LICH_SU, "w") as f:
        json.dump(da_gui, f)

def lay_ket_qua(league_id):
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id={league_id}"
    response = requests.get(url)
    data = response.json()
    return data.get("events", [])

def gui_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def kiem_tra_va_gui():
    print("⏳ Đang kiểm tra kết quả mới...")
    da_gui = doc_lich_su()

    for ten_giai, league_id in GIAI_DAU.items():
        events = lay_ket_qua(league_id)
        if not events:
            continue

        tin = f"*{ten_giai}*\n\n"
        co_moi = False

        for match in events[:5]:
            home = match.get("strHomeTeam", "")
            away = match.get("strAwayTeam", "")
            score_home = match.get("intHomeScore", "?")
            score_away = match.get("intAwayScore", "?")
            date = match.get("dateEvent", "")
            match_id = match.get("idEvent", "")

            if not home or not away or not match_id:
                continue
            if match_id in da_gui:
                continue

            tin += f"📅 {date}\n"
            tin += f"🏟 {home} {score_home} - {score_away} {away}\n"
            tin += "➖➖➖➖➖➖\n"
            da_gui.append(match_id)
            co_moi = True

        if co_moi:
            gui_telegram(tin)
            print(f"✅ Gửi mới: {ten_giai}")

    luu_lich_su(da_gui)
    print("✔ Kiểm tra xong!\n")

# Chạy ngay lần đầu
kiem_tra_va_gui()

# Sau đó kiểm tra mỗi 30 phút
schedule.every(30).minutes.do(kiem_tra_va_gui)

print("🤖 Bot đang chạy... (Ctrl+C để dừng)")
while True:
    schedule.run_pending()
    time.sleep(60)
