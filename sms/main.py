from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_reply():
    incoming_msg = request.form.get('Body').strip().lower()

    # Here you can customize your logic. For example:
    if 'how busy' in incoming_msg:
        status = get_status()
    else:
        status = "Please send 'How Busy ?' to get a response."

    resp = MessagingResponse()
    resp.message(status)
    return str(resp)

def get_status():
    # Replace this with your logic to determine the busy status
    return "kinda busy"  # This is just a placeholder

if __name__ == '__main__':
    # Run the Flask app locally for testing
    app.run(debug=True)

