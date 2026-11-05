import os
import time
from datetime import datetime
import random
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram Token or Chat ID is missing!")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending telegram message: {e}")

TRACKER_FILE = "session_tracker.txt"

def get_completed_sessions():
    if not os.path.exists(TRACKER_FILE):
        return []
    with open(TRACKER_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        date_str, sessions_str = content.split("|")
        today = datetime.now().strftime("%Y-%m-%d")
        if date_str != today:
            return []
        return sessions_str.split(",") if sessions_str else []

def mark_session_completed(session_name):
    today = datetime.now().strftime("%Y-%m-%d")
    completed = get_completed_sessions()
    if session_name not in completed:
        completed.append(session_name)
    with open(TRACKER_FILE, "w") as f:
        f.write(f"{today}|{','.join(completed)}")

def run_vip_session(session_number_str, session_name):
    completed = get_completed_sessions()
    if session_name in completed:
        return 

    print(f"Starting {session_name}...")
    
    live_msg = f"""🚨 VIP SESSION IS LIVE NOW! 🟢🔥

⚡ SESSION HAS STARTED! ({session_name})

"Keep your focus high and emotions low. Patience pays!" 🎯📈

💻 STATUS -: Session In Progress

⏳ ACTION -: Wait for the Signal!

🛡️ RULE -: Strict Money Management (2%-5% Capital)

📢 Keep your terminals open and stay alert! First trade signal is dropping any second... 🚀💰"""
    send_telegram_message(live_msg)
    time.sleep(10)

    pairs = [
        "EUR/USD", "GBP/JPY", "AUD/CAD", "USD/CHF",
        "EUR/GBP", "NZD/USD", "BTC/USDT", "USD/JPY",
        "EUR/JPY", "AUD/USD", "GBP/USD", "USD/CAD"
    ]
    directions = ["🟢 CALL (UP)", "🔴 PUT (DOWN)"]
    timeframes = ["1 Minute", "5 Minutes"]

    trade_results_log = []
    total_wins = 0
    total_losses = 0

    for i in range(1, 13):
        pair = pairs[i - 1]
        direction = random.choice(directions)
        tf = random.choice(timeframes)

        signal_msg = f"""📊 TRADE SIGNAL SETUP

PAIR NAME -: {pair}

TIME FRAME -: {tf}

DIRECTION -: {direction}

⚠️ MONEY MANAGEMENT RULE:
Always use proper risk management (Max 2% to 5% of your total capital per trade). Stick to a disciplined martingale plan only if your strategy requires it, and never chase losses blindly! 🚀💰"""
        send_telegram_message(signal_msg)
        time.sleep(20)

        is_win = random.choices([True, False], weights=[80, 20])[0]
        if is_win:
            total_wins += 1
            result_type = random.choice(["🟢 WIN (Direct)", "🟢 WIN (MTG 1)"])
        else:
            total_losses += 1
            result_type = "🔴 LOSS"

        trend_icon = "📈" if "UP" in direction else "📉"
        trade_results_log.append(f"{trend_icon} {pair} | {'UP' if 'UP' in direction else 'DOWN'} ➔ {result_type}")

        accuracy_str = "85% / " + ("Direct Win" if "Direct" in result_type else "Martingale")
        result_msg = f"""📊 TRADE RESULT UPDATE

TRADE RESULT -: {'🟢 PROFIT (ITM)' if is_win else '🔴 LOSS (OTM)'}

TRADE ACCURACY -: {accuracy_str}
💡 PRO TIP: Market mein losses bhi trading ka part hote hain. Proper money management (2%-5%) aur compound discipline hi long-term success ki key hai! 🚀💰"""
        send_telegram_message(result_msg)
        time.sleep(10)

    close_msg = f"""🔴 VIP SESSION CLOSED! 🔚✨

📊 SESSION COMPLETED ({session_name})

"Consistency over intensity. Secure your profit and exit the market!" 🎯📈

💼 STATUS -: All Trades Wrapped Up

🛡️ RULE -: Close your terminal now — Do NOT overtrade!

🧠 MINDSET -: Respect your daily target and protect your capital.

🎉 Great job today, team! Take your profits, relax, and get ready for the next session. See you soon! 🚀💰"""
    send_telegram_message(close_msg)
    time.sleep(5)

    accuracy_calc = round((total_wins / 12) * 100, 1)
    scorecard_lines = "\n".join(trade_results_log)

    scorecard_msg = f"""🔥 VIP BOT SESSION RESULTS 🔥

🤖 {session_number_str} Bot Session Result -:

{scorecard_lines}

📊 SESSION SUMMARY
🎯 TOTAL TRADES -: 12
🟢 TOTAL WINS -: {total_wins}
🔴 TOTAL LOSSES -: {total_losses}

⚡ SESSION ACCURACY -: {accuracy_calc}%

💰 PROFIT ALERT: Target achieved for this session! Strict money management applied. 🚀💸"""
    send_telegram_message(scorecard_msg)

    mark_session_completed(session_name)

def check_notifications():
    now = datetime.now()
    hour = now.hour

    if hour == 7:
        run_special_once("morning_briefing", lambda: send_telegram_message("""🌅 RISE AND SHINE TRADERS! ☕🔥

🌟 MORNING BRIEFING & FOCUS

"Consistency is the bridge between goals and wealth." 💎📈

🎯 MINDSET -: Calm, Focused & Disciplined
⚠️ REMINDER -: Never chase losses. Protect capital first!

🚀 MISSION -: Follow the signals, execute with precision, and secure the profits.

⏰ Get your terminals ready! Today's VIP sessions are locked and loaded. Let's start the day in pure GREEN! 💸🍀"""))

    if hour == 8:
        run_special_once("schedule_msg", lambda: send_telegram_message("""👑 TODAY BOT SESSION SCHEDULE 👑

⏰ DAILY SESSION TIMINGS

🌅 1st Session -: 09:00 AM

☀️ 2nd Session -: 12:00 PM

🌤️ 3rd Session -: 02:00 PM

🌇 4th Session -: 06:00 PM

🌙 5th Session -: 11:00 PM

⚠️ IMPORTANT NOTE: Be online 5 minutes before the session time! Follow strict money management and protect your capital. 🚀💰"""))

    if hour == 0:
        run_special_once("night_wrap", lambda: send_telegram_message("""GOOD NIGHT VIP FAMILY! 🌌✨

💤 END OF DAY WRAP-UP

"Discipline today brings financial freedom tomorrow." 💎📈

📊 TODAY'S STATUS -: 
Market Closed / Sessions Completed

🧠 MINDSET -: Rest well, recharge, and come back stronger tomorrow.

🛡️ REMINDER -: Protect your peace and your capital. Tomorrow is a new opportunity!

⭐ Sleep tight and get ready for another massive green day ahead! Good night, traders! 🚀💰"""))

    if hour == 9:
        run_vip_session("1st", "09:00 AM Session")
    elif hour == 12:
        run_vip_session("2nd", "12:00 PM Session")
    elif hour == 14:
        run_vip_session("3rd", "02:00 PM Session")
    elif hour == 18:
        run_vip_session("4th", "06:00 PM Session")
    elif hour == 23:
        run_vip_session("5th", "11:00 PM Session")

def run_special_once(key, func):
    tracker_file = "special_tracker.txt"
    today = datetime.now().strftime("%Y-%m-%d")
    completed = []
    if os.path.exists(tracker_file):
        with open(tracker_file, "r") as f:
            content = f.read().strip()
            if content:
                d, keys = content.split("|")
                if d == today:
                    completed = keys.split(",") if keys else []
    
    if key not in completed:
        func()
        completed.append(key)
        with open(tracker_file, "w") as f:
            f.write(f"{today}|{','.join(completed)}")

if __name__ == "__main__":
    check_notifications()
      
