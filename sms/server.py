from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from howBusy import get_status_from_file
from datetime import datetime

app = Flask(__name__)

def get_meal_name_by_time():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    current_minutes = hour * 60 + minute

    if 420 <= current_minutes <= 630:     # 7:00 AM to 10:30 AM
        return "Breakfast"
    elif 660 <= current_minutes <= 870:   # 11:00 AM to 2:30 PM
        return "Lunch"
    elif 990 <= current_minutes <= 1200:  # 4:30 PM to 8:00 PM
        return "Dinner"
    elif 420 <= current_minutes <= 1200:  # Between 7 AM and 8 PM
        return "Afternoon Snack"
    else:
        return "Closed"

def get_meal_section(meal_name):
    try:
        with open("menu.txt", "r") as f:
            lines = f.readlines()

        output = []
        found = False
        for line in lines:
            if line.strip() == f"{meal_name}:":
                found = True
                output.append(line.strip())
                continue
            if found:
                if line.strip() == "":
                    break
                output.append(line.rstrip())
        return "\n".join(output) if output else "Sorry, no items found."
    except:
        return "Sorry, menu is currently unavailable."

@app.route("/sms", methods=['POST'])
def sms_reply():
    incoming_msg = request.form.get('Body', '').strip().lower()
    print("💬 Received SMS:", incoming_msg)

    resp = MessagingResponse()

    if "how busy" in incoming_msg:
        status = get_status_from_file()
        print("How Busy:", status)
        resp.message(f"How Busy: {status}")
    
    elif "what's cooking" in incoming_msg or "whats cooking" in incoming_msg:
        meal = get_meal_name_by_time()
        if meal == "Closed":
            resp.message("😴 The kitchen is currently closed.")
        else:
            menu_text = get_meal_section(meal)
            resp.message(f"🍽️ {meal} Menu:\n{menu_text}")

    else:
        resp.message("Send 'How busy?' or 'What's cooking?' to get info.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
