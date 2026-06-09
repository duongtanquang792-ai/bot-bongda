import requests
import schedule
import time
import json
import os
from datetime import date

TOKEN = "8662302479:AAGoR8ZMMvzl0bzO_Ui-3-Gj0pfpBzUewQs"
CHANNEL = "@demokenh"
FILE_LICH_SU = "lich_su.json"

def doc_lich_su():
    if os.path.exists(FILE_LICH_SU):
        with open(FILE_LICH_SU, "r") as f:
            return json.load(f)
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

def kiem_tra_va_gui():
    print("⏳ Đang kiểm tra kết quả hôm nay...")
    hom_nay = date.today().strftime("%Y-%m-%d")
    da_gui = doc_lich_su()

    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={hom_nay}&s=Soccer"
    response = requests.get(url)
    data = response.json()
    events = data.get("events") or []

    if not events:
        print("Hôm nay chưa có trận nào.")
        return

    tin = f"⚽ *KẾT QUẢ BÓNG ĐÁ HÔM NAY {hom_nay}*\n\n"
    co_moi = False

    for match in events:
        home = match.get("strHomeTeam", "")
        away = match.get("strAwayTeam", "")
        score_home = match.get("intHomeScore")
        score_away = match.get("intAwayScore")
        league = match.get("strLeague", "")
        match_id = match.get("idEvent", "")

        if not home or not away or not match_id:
            continue
        if match_id in da_gui:
            continue
        if score_home is None or score_away is None:
            continue

        tin += f"🏆 {league}\n"
        tin += f"🏟 {home} {score_home} - {score_away} {away}\n"
        tin += "➖➖➖➖➖➖\n"
        da_gui.append(match_id)
        co_moi = True

    if co_moi:
        gui_telegram(tin)
        print("✅ Đã gửi kết quả mới!")
    else:
        print("Không có kết quả mới.")

    luu_lich_su(da_gui)

# Chạy ngay lần đầu
kiem_tra_va_gui()

# Kiểm tra mỗi 30 phút
schedule.every(30).minutes.do(kiem_tra_va_gui)

print("🤖 Bot đang chạy 24/24...")
while True:
    schedule.run_pending()
    time.sleep(60)
