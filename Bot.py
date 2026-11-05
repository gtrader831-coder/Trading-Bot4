import os
import time
from datetime import datetime
import random
import requests

# Telegram credentials from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram_message(message):
  """Function to send message to Telegram channel"""
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("Telegram Token or Chat ID is missing!")
    return
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": message,
      "parse_mode": "Markdown",
  }
  try:
    response = requests.post(url, json=payload)
    if response.status_code != 200:
      print(f"Failed to send message: {response.text}")
  except Exception as e:
    print(f"Error sending telegram message: {e}")


# Track sent daily notifications to avoid duplicate triggers in the same minute
last_sent_morning = ""
last_sent_schedule = ""
last_sent_night = ""


def check_daily_notifications():
  global last_sent_morning, last_sent_schedule, last_sent_night
  now = datetime.now()
  current_date = now.strftime("%Y-%m-%d")
  current_time = now.strftime("%H:%M")

  # 1. Subah 7:00 AM Morning Briefing
  if current_time == "07:00" and last_sent_morning != current_date:
    msg = """🌅 RISE AND SHINE TRADERS! ☕🔥

🌟 MORNING BRIEFING & FOCUS

"Consistency is the bridge between goals and wealth." 💎📈

🎯 MINDSET -: Calm, Focused & Disciplined
⚠️ REMINDER -: Never chase losses. Protect capital first!

🚀 MISSION -: Follow the signals, execute with precision, and secure the profits.

⏰ Get your terminals ready! Today's VIP sessions are locked and loaded. Let's start the day in pure GREEN! 💸🍀"""
    send_telegram_message(msg)
    last_sent_morning = current_date

  # 2. Subah 8:00 AM Session Schedule
  if current_time == "08:00" and last_sent_schedule != current_date:
    msg = """👑 TODAY BOT SESSION SCHEDULE 👑

⏰ DAILY SESSION TIMINGS

🌅 1st Session -: 09:00 AM

☀️ 2nd Session -: 12:00 PM

🌤️ 3rd Session -: 02:00 PM

🌇 4th Session -: 06:00 PM

🌙 5th Session -: 11:00 PM

⚠️ IMPORTANT NOTE: Be online 5 minutes before the session time! Follow strict money management and protect your capital. 🚀💰"""
    send_telegram_message(msg)
    last_sent_schedule = current_date

  # 3. Raat 12:00 AM (00:00) Good Night Wrap-up
  if current_time == "00:00" and last_sent_night != current_date:
    msg = """GOOD NIGHT VIP FAMILY! 🌌✨

💤 END OF DAY WRAP-UP

"Discipline today brings financial freedom tomorrow." 💎📈

📊 TODAY'S STATUS -: 
Market Closed / Sessions Completed

🧠 MINDSET -: Rest well, recharge, and come back stronger tomorrow.

🛡️ REMINDER -: Protect your peace and your capital. Tomorrow is a new opportunity!

⭐ Sleep tight and get ready for another massive green day ahead! Good night, traders! 🚀💰"""
    send_telegram_message(msg)
    last_sent_night = current_date


def run_vip_session(session_number_str, session_name):
  """Runs a full VIP session with 12 trades and summary scorecard"""
  # Session Live Alert
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
  directions = ["🟢 CALL (UP)", "🔴 PUT (DOWN)"]
  timeframes = ["1 Minute", "5 Minutes"]

  trade_results_log = []
  total_wins = 0
  total_losses = 0

  # Simulating 12 trades in the session
  for i in range(1, 13):
    pair = pairs[i - 1]
    direction = random.choice(directions)
    tf = random.choice(timeframes)

    # Send Signal Setup
    signal_msg = f"""📊 TRADE SIGNAL SETUP

PAIR NAME -: {pair}

TIME FRAME -: {tf}

DIRECTION -: {direction}

⚠️ MONEY MANAGEMENT RULE:
Always use proper risk management (Max 2% to 5% of your total capital per trade). Stick to a disciplined martingale plan only if your strategy requires it, and never chase losses blindly! 🚀💰"""
    send_telegram_message(signal_msg)

    # Wait between trade execution & result simulation (e.g., 30 seconds for bot loop)
    time.sleep(30)

    # Simulate win/loss outcome
    is_win = random.choices([True, False], weights=[80, 20])[0]
    if is_win:
      total_wins += 1
      result_type = random.choice(
          ["🟢 WIN (Direct)", "🟢 WIN (MTG 1)", "🟢 WIN (MTG 2)"]
      )
    else:
      total_losses += 1
      result_type = "🔴 LOSS"

    trend_icon = "📈" if "UP" in direction else "📉"
    trade_results_log.append(f"{trend_icon} {pair} | {'UP' if 'UP' in direction else 'DOWN'} ➔ {result_type}")

    # Send Individual Trade Result Update
    accuracy_str = "85% / " + ("Direct Win" if "Direct" in result_type else "Martingale")
    result_msg = f"""📊 TRADE RESULT UPDATE

TRADE RESULT -: {'🟢 PROFIT (ITM)' if is_win else '🔴 LOSS (OTM)'}

TRADE ACCURACY -: {accuracy_str}
💡 PRO TIP: Market mein losses bhi trading ka part hote hain. Proper money management (2%-5%) aur compound discipline hi long-term success ki key hai! 🚀💰"""
    send_telegram_message(result_msg)
    time.sleep(15)

  # Session Closed Message
  close_msg = f"""🔴 VIP SESSION CLOSED! 🔚✨

📊 SESSION COMPLETED ({session_name})

"Consistency over intensity. Secure your profit and exit the market!" 🎯📈

💼 STATUS -: All Trades Wrapped Up

🛡️ RULE -: Close your terminal now — Do NOT overtrade!

🧠 MINDSET -: Respect your daily target and protect your capital.

🎉 Great job today, team! Take your profits, relax, and get ready for the next session. See you soon! 🚀💰"""
  send_telegram_message(close_msg)
  time.sleep(10)

  # Final Session Scorecard Summary
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


# Main loop to check schedules continuously via GitHub Actions cron or long-polling execution
def main():
  while True:
    check_daily_notifications()
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    # Session Time Triggers
    if current_time == "09:00":
      run_vip_session("1st", "09:00 AM Session")
      time.sleep(60)  # Prevent duplicate triggers within the same minute
    elif current_time == "12:00":
      run_vip_session("2nd", "12:00 PM Session")
      time.sleep(60)
    elif current_time == "14:00":
      run_vip_session("3rd", "02:00 PM Session")
      time.sleep(60)
    elif current_time == "18:00":
      run_vip_session("4th", "06:00 PM Session")
      time.sleep(60)
    elif current_time == "23:00":
      run_vip_session("5th", "11:00 PM Session")
      time.sleep(60)

    time.sleep(30)  # Check every 30 seconds


if __name__ == "__main__":
  main()
    
