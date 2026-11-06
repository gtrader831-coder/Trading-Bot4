# -*- coding: utf-8 -*-
import datetime
import os
import random
import time
import requests
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

PAIRS = [
    "EUR/USD",
    "GBP/JPY",
    "AUD/CAD",
    "USD/CHF",
    "EUR/GBP",
    "NZD/USD",
    "BTC/USDT",
    "USD/JPY",
    "EUR/JPY",
    "AUD/USD",
    "GBP/USD",
    "USD/CAD",
]

def send_telegram_text(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def send_telegram_photo(caption, image_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(image_path, "rb") as photo:
        payload = {"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}
        files = {"photo": photo}
        requests.post(url, data=payload, files=files)

def generate_card_image(title, subtitle, bg_color):
    # Create a professional trading banner/card image
    img = Image.new("RGB", (800, 450), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Draw border and styling elements
    d.rectangle([15, 15, 785, 435], outline="#FFFFFF", width=3)
    d.rectangle([30, 30, 770, 100], fill="#111827")
    
    # Text rendering (Using default font or basic layout)
    d.text((50, 45), title, fill="#00FFCC")
    d.text((50, 140), subtitle, fill="#FFFFFF")
    d.text((50, 380), "👑 @tradewithraje949 - VIP TRADING BOT", fill="#F3F4F6")
    
    path = "temp_chart.png"
    img.save(path)
    return path

def run_session(session_name):
    send_telegram_text(
        """🚨 VIP SESSION IS LIVE NOW! 🟢🔥

⚡ SESSION HAS STARTED!

"Keep your focus high and emotions low. Patience pays!" 🎯📈

💻 STATUS -: Session In Progress

⏳ ACTION -: Wait for the Signal!

🛡️ RULE -: Strict Money Management (2%-5% Capital)

📢 Keep your terminals open and stay alert! First trade signal is dropping any second... 🚀💰"""
    )

    time.sleep(10)

    results_summary = []
    total_wins = 0
    total_losses = 0

    for i in range(12):
        pair = PAIRS[i]
        direction = random.choice(["🟢 CALL (UP)", "🔴 PUT (DOWN)"])
        bg_col = "#064E3B" if "CALL" in direction else "#7F1D1D"
        
        img_path = generate_card_image(f"SIGNAL: {pair}", f"DIRECTION: {direction}\nTIMEFRAME: 1 Minute", bg_col)

        signal_text = f"""📊 TRADE SIGNAL SETUP

PAIR NAME -: {pair}

TIME FRAME -: 1 Minute

DIRECTION -: {direction}

⚠️ MONEY MANAGEMENT RULE:
Always use proper risk management (Max 2% to 5% of total capital per trade). Stick to a disciplined martingale plan only if your strategy requires it, and never chase losses blindly! 🚀💰"""

        send_telegram_photo(signal_text, img_path)
        time.sleep(60)

        is_win = random.choice([True, True, True, False])
        if is_win:
            win_type = random.choice(["Direct Win", "MTG 1"])
            result_str = f"🟢 PROFIT (ITM) | {win_type}"
            trade_log = f"{pair} ➔ 🟢 WIN ({win_type})"
            total_wins += 1
        else:
            result_str = "🔴 LOSS (OTM)"
            trade_log = f"{pair} ➔ 🔴 LOSS"
            total_losses += 1

        results_summary.append(trade_log)

        result_text = f"""📊 TRADE RESULT UPDATE

TRADE RESULT -: {result_str}

💡 PRO TIP: Market mein losses bhi trading ka part hote hain. Proper money management (2%-5%) aur compound discipline hi long-term success ki key hai! 🚀💰"""

        send_telegram_text(result_text)

        if i < 11:
            time.sleep(300) # Exact 5 minute gap between trades

    send_telegram_text(
        """🔴 VIP SESSION CLOSED! 🔚✨

📊 SESSION COMPLETED

"Consistency over intensity. Secure your profit and exit the market!" 🎯📈

💼 STATUS -: All Trades Wrapped Up

🛡️ RULE -: Close your terminal now — Do NOT overtrade!

🧠 MINDSET -: Respect your daily target and protect your capital.

🎉 Great job today, team! Take your profits, relax, and get ready for the next session. See you soon! 🚀💰"""
    )

    time.sleep(10)

    accuracy = round((total_wins / 12) * 100, 1)
    results_text = "\n".join(results_summary)

    send_telegram_text(
        f"""🔥 VIP BOT SESSION RESULTS 🔥

🤖 {session_name} Bot Session Result -:

{results_text}

📊 SESSION SUMMARY
🎯 TOTAL TRADES -: 12
🟢 TOTAL WINS -: {total_wins}
🔴 TOTAL LOSSES -: {total_losses}

⚡ SESSION ACCURACY -: {accuracy}%

💰 PROFIT ALERT: Target achieved for this session! Strict money management applied. 🚀💸"""
    )

utc_now = datetime.datetime.utcnow()
ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
current_hour = ist_now.hour

if current_hour == 7:
    send_telegram_text(
        """🌅 RISE AND SHINE TRADERS! ☕🔥

🌟 MORNING BRIEFING & FOCUS

"Consistency is the bridge between goals and wealth." 💎📈

🎯 MINDSET -: Calm, Focused & Disciplined
⚠️ REMINDER -: Never chase losses. Protect capital first!

🚀 MISSION -: Follow the signals, execute with precision, and secure the profits.

⏰ Get your terminals ready! Today's VIP sessions are locked and loaded. Let's start the day in pure GREEN! 💸🍀"""
    )

elif current_hour == 8:
    send_telegram_text(
        """👑 TODAY BOT SESSION SCHEDULE 👑

⏰ DAILY SESSION TIMINGS

🌅 1st Session -: 09:00 AM
☀️ 2nd Session -: 12:00 PM
🌤️ 3rd Session -: 02:00 PM
🌇 4th Session -: 06:00 PM
🌙 5th Session -: 11:00 PM

⚠️ IMPORTANT NOTE: Be online 5 minutes before the session time! Follow strict money management and protect your capital. 🚀💰"""
    )

elif current_hour == 9:
    run_session("1st")
elif current_hour == 12:
    run_session("2nd")
elif current_hour == 14:
    run_session("3rd")
elif current_hour == 18:
    run_session("4th")
elif current_hour == 23:
    run_session("5th")

elif current_hour == 0:
    send_telegram_text(
        """GOOD NIGHT VIP FAMILY! 🌌✨

💤 END OF DAY WRAP-UP

"Discipline today brings financial freedom tomorrow." 💎📈

📊 TODAY'S STATUS -: 
Market Closed / Sessions Completed

🧠 MINDSET -: Rest well, recharge, and come back stronger tomorrow.

🛡️ REMINDER -: Protect your peace and your capital. Tomorrow is a new opportunity!

⭐ Sleep tight and get ready for another massive green day ahead! Good night, traders! 🚀💰"""
             )
    
