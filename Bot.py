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
    
    live_msg = f"🚨 VIP SESSION IS LIVE NOW! 🟢🔥\n\n⚡ SESSION HAS STARTED! ({session_name})\n\n\"Keep your focus high and emotions low. Patience pays!\" 🎯📈\n\n💻 STATUS -: Session In Progress\n\n⏳ ACTION -: Wait for the Signal!\n\n🛡️ RULE -: Strict Money Management (2%-5% Capital)\n\n📢 Keep your terminals open and stay alert! First trade signal is dropping any second... 🚀💰"
    send_telegram_message(live_msg)
    time.sleep(10)

    pairs = [
        "EUR/USD", "GBP/JPY", "AUD/CAD", "USD/CHF",
        "EUR/GBP", "NZD/USD", "BTC/USDT", "USD/JPY",
        "EUR/JPY", "AUD/USD", "GBP/USD", "USD/CAD"
    ]
    directions = ["🟢 CALL (UP)", "🔴 PUT (DOWN)"]
    timeframes = ["1 Minute", "5 Minutes"]

    for i in range(1, 13):
        pair = pairs[i - 1]
        direction = random.choice(directions)
        tf = random.choice(timeframes)

        signal_msg = f"📊 TRADE SIGNAL SETUP\n\nPAIR NAME -: {pair}\n\nTIME FRAME -: {tf}\n\nDIRECTION -: {direction}\n\n⚠️ MONEY MANAGEMENT RULE:\nAlways use proper risk management (Max 2% to 5% of your total capital per trade). Stick to a disciplined martingale plan only if your strategy requires it, and never chase losses blindly! 🚀💰"
        send_telegram_message(signal_msg)
        time.sleep(20)

        is_win = random.choices([True, False], weights=[80, 20])[0]
        result_type = "🟢 WIN (Direct)" if is_win else "🔴 LOSS"

        accuracy_str = "85% / Direct Win" if is_win else "85% / Martingale"
        result_msg = f"📊 TRADE RESULT UPDATE\n\nTRADE RESULT -: {'🟢 PROFIT (ITM)' if is_win else '🔴 LOSS (OTM)'}\n\nTRADE ACCURACY -: {accuracy_str}\n💡 PRO TIP: Market mein losses bhi trading ka part hote hain. Proper money management (2%-5%) aur compound discipline hi long-term success ki key hai! 🚀💰"
        send_telegram_message(result_msg)
        time.sleep(10)

    # 1. Session Closed Message
    close_msg = f"🔴 VIP SESSION CLOSED! 🔚✨\n\n📊 SESSION COMPLETED ({session_name})\n\n\"Consistency over intensity. Secure your profit and exit the market!\" 🎯📈\n\n💼 STATUS -: All Trades Wrapped Up\n\n🛡️ RULE -: Close your terminal now — Do NOT overtrade!\n\n🧠 MINDSET -: Respect your daily target and protect your capital.\n\n🎉 Great job today, team! Take your profits, relax, and get ready for the next session. See you soon! 🚀💰"
    send_telegram_message(close_msg)
    time.sleep(5)

    # 2. Exact Scorecard Format with Dynamic Session Number
    scorecard_msg = f"""🔥 VIP BOT SESSION RESULTS 🔥
🤖 {session_number_str} Bot Session Result -:
 * 📈 EUR/USD | UP ➔ 🟢 WIN (Direct)
 * 📉 GBP/JPY | DOWN ➔ 🟢 WIN (Direct)
 * 📈 AUD/CAD | UP ➔ 🔴 LOSS
 * 📉 USD/CHF | DOWN ➔ 🟢 WIN (MTG 1)
 * 📈 EUR/GBP | UP ➔ 🟢 WIN (Direct)
 * 📉 NZD/USD | DOWN ➔ 🟢 WIN (Direct)
 * 📈 BTC/USDT | UP ➔ 🟢 WIN (MTG 1)
 * 📉 USD/JPY | DOWN ➔ 🔴 LOSS
 * 📈 EUR/JPY | UP ➔ 🟢 WIN (Direct)
 * 📉 AUD/USD | DOWN ➔ 🟢 WIN (Direct)
 * 📈 GBP/USD | UP ➔ 🟢 WIN (MTG 1)
 * 📉 USD/CAD | DOWN ➔ 🟢 WIN (Direct)
📊 SESSION SUMMARY
 * 🎯 TOTAL TRADES -: 12
 * 🟢 TOTAL WINS -: 10
 * 🔴 TOTAL LOSSES -: 2
 * ⚡ SESSION ACCURACY -: 83.3%
> 💰 PROFIT ALERT: Target achieved for this session! Strict money management applied. 🚀💸"""
    send_telegram_message(scorecard_msg)

    mark_session_completed(session_name)

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

def check_notifications():
    now = datetime.now()
    hour = now.hour

    if hour == 7:
        run_special_once("morning_briefing", lambda: send_telegram_message("🌅 RISE AND SHINE TRADERS! ☕🔥\n\n🌟 MORNING BRIEFING & FOCUS\n\n\"Consistency is the bridge between goals and wealth.\" 💎📈\n\n🎯 MINDSET -: Calm, Focused & Disciplined\n⚠️ REMINDER -: Never chase losses. Protect capital first!\n\n🚀 MISSION -: Follow the signals, execute with precision, and secure the profits.\n\n⏰ Get your terminals ready! Today's VIP sessions are locked and loaded. Let's start the day in pure GREEN! 💸🍀"))

    if hour == 8:
        run_special_once("schedule_msg", lambda: send_telegram_message("👑 TODAY BOT SESSION SCHEDULE 👑\n\n⏰ DAILY SESSION TIMINGS\n\n🌅 1st Session -: 09:00 AM\n\n☀️ 2nd Session -: 12:00 PM\n\n🌤️ 3rd Session -: 02:00 PM\n\n🌇 4th Session -: 06:00 PM\n\n🌙 5th Session -: 11:00 PM\n\n⚠️ IMPORTANT NOTE: Be online 5 minutes before the session time! Follow strict money management and protect your capital. 🚀💰"))

    if hour == 0:
        run_special_once("night_wrap", lambda: send_telegram_message("GOOD NIGHT VIP FAMILY! 🌌✨\n\n💤 END OF DAY WRAP-UP\n\n\"Discipline today brings financial freedom tomorrow.\" 💎📈\n\n📊 TODAY'S STATUS -: \nMarket Closed / Sessions Completed\n\n🧠 MINDSET -: Rest well, recharge, and come back stronger tomorrow.\n\n🛡️ REMINDER -: Protect your peace and your capital. Tomorrow is a new opportunity!\n\n⭐ Sleep tight and get ready for another massive green day ahead! Good night, traders! 🚀💰"))

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

if __name__ == "__main__":
    check_notifications()
    
