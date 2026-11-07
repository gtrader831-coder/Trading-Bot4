import datetime
import json
import os
import time

# State file to prevent duplicate runs on the same day
STATE_FILE = "session_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def can_run_task(task_name):
    today = datetime.date.today().isoformat()
    state = load_state()
    if state.get(task_name) == today:
        return False  
    return True

def mark_task_completed(task_name):
    today = datetime.date.today().isoformat()
    state = load_state()
    state[task_name] = today
    save_state(state)

def send_telegram_message(text):
    # Yahan apna Telegram API / Bot message send karne ka code lagayein
    print(f"\n[TELEGRAM BROADCAST]:\n{text}\n")

# 1. Morning Briefing (7:00 AM)
def send_morning_briefing():
    if not can_run_task("morning_briefing"):
        return
    
    msg = (
        "🌅 **GOOD MORNING TRADERS!** ☕✨\n\n"
        "Naye din ki shuruaat ek nayi energy aur positive mindset ke sath hoti hai. "
        "Aaj ka din aapke liye profit bhara ho!\n\n"
        "📅 **Aaj ke sabhi VIP Sessions ka Schedule:**\n"
        "• 09:00 AM - Morning VIP Session\n"
        "• 12:00 PM - Afternoon VIP Session\n"
        "• 02:00 PM - Mid-Day VIP Session\n"
        "• 06:00 PM - Evening VIP Session\n"
        "• 11:00 PM - Night VIP Session\n\n"
        "⚠️ **Risk Warning:** Hamesha apne risk management aur capital ke hisab se trade karein. Let's make it profitable! 🚀📈"
    )
    send_telegram_message(msg)
    mark_task_completed("morning_briefing")

# 2. Complete Trading Session (Start Notice, Pair Name, 12 Trades with Results, Summary & Final Scorecard)
def run_vip_session(session_name, session_key, pair_name="EUR/USD (OTC)"):
    if not can_run_task(session_key):
        print(f"[{session_name}] Aaj ke liye already run ho chuka hai. Dobara nahi chalega!")
        return

    print(f"--- Starting {session_name} ---")
    
    # Session Start Notice
    start_msg = (
        f"🟢 **{session_name} is LIVE Now!** 🚀🔔\n\n"
        f"🎯 **Trading Pair:** `{pair_name}`\n"
        f"⚡ Sabhi log ready ho jayein, kuch hi der mein signals aane shuru honge!"
    )
    send_telegram_message(start_msg)
    time.sleep(2)
    
    wins = 0
    losses = 0
    total_trades = 12
    trade_history = []  # Har trade ka result store karne ke liye

    # 12 Trades Loop with Pair Name & Trade Results
    for trade_no in range(1, total_trades + 1):
        # Advance Signal Alert
        signal_msg = (
            f"📊 **{session_name} | Trade #{trade_no} / {total_trades}** ⚡🎯\n"
            f"🔹 **Pair:** `{pair_name}`\n"
            f"⏳ Get Ready for Action (Next 1-Minute Candle)!"
        )
        send_telegram_message(signal_msg)
        time.sleep(3)  # Simulation for trade duration / candle run
        
        # Simulated Result (WIN/LOSS)
        result = "WIN 💰" if trade_no % 4 != 0 else "LOSS ❌"  
        if "WIN" in result:
            wins += 1
        else:
            losses += 1

        trade_history.append(f"Trade #{trade_no}: {result}")

        result_msg = (
            f"✨ **Trade #{trade_no} Result Update** ✨\n"
            f"🔹 **Pair:** `{pair_name}`\n"
            f"📌 **Status:** {result}"
        )
        send_telegram_message(result_msg)
        time.sleep(2)  # 5-minute technical gap simulation between trades

    # Session Close Summary Report
    accuracy = round((wins / total_trades) * 100, 2)
    summary_msg = (
        f"🔴 **{session_name} CLOSED** 🛑\n\n"
        f"📊 **Session Summary Report:**\n"
        f"🔹 **Pair:** `{pair_name}`\n"
        f"🎯 **Total Trades:** {total_trades}\n"
        f"✅ **Total Wins:** {wins}\n"
        f"❌ **Total Losses:** {losses}\n"
        f"⭐ **Accuracy:** `{accuracy}%`"
    )
    send_telegram_message(summary_msg)
    time.sleep(1)

    # Session Close ke Baad Pura Final Detailed Result & Scorecard
    history_str = "\n".join(trade_history)
    final_scorecard_msg = (
        f"🏆 **{session_name} - FINAL DETAILED SCORECARD** 📈💎\n\n"
        f"🔹 **Trading Pair:** `{pair_name}`\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"{history_str}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Final Score:** `{wins} Wins` / `{losses} Losses`\n"
        f"🔥 **Overall Accuracy:** `{accuracy}%`\n\n"
        f"Shandar session raha! Sabhi ne acha profit banaya hoga. Agle session mein milte hain! 🙏✨"
    )
    send_telegram_message(final_scorecard_msg)
    
    # Lock this session for the day so it never repeats automatically
    mark_task_completed(session_key)
    print(f"--- {session_name} Completed & Locked for Today ---")

# 3. Night Wrap-up (End of Day)
def send_night_wrapup():
    if not can_run_task("night_wrapup"):
        return
    
    msg = (
        "🌌 **GOOD NIGHT TRADERS!** 💤💎\n\n"
        "Aaj ke sabhi VIP sessions successfully complete ho chuke hain. Ummeed hai aapne acha profit banaya hoga.\n\n"
        "Apna dhyan rakhein, relax karein aur kal subah phir ek nayi energy ke sath milte hain. Sweet dreams! 🌟✨"
    )
    send_telegram_message(msg)
    mark_task_completed("night_wrapup")

# Main Execution / Scheduler Trigger Example
if __name__ == "__main__":
    send_morning_briefing()
    run_vip_session("09:00 AM VIP Session", "session_09_00", "EUR/USD (OTC)")
    # Baki sessions (12:00 PM, 02:00 PM, 06:00 PM, 11:00 PM) ke liye bhi yhi function call hoga
    send_night_wrapup()
    
