import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import google.generativeai as genai

load_dotenv()

app = App(token=os.environ["SLACK_TOKEN"])
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Pehla function bahar hona chahiye
@app.event("message")
def handle_message_events(event, say):
    if "user" in event:
        say(f"Maine aapka message sun liya: {event['text']}")

# Dusra function bhi alag hona chahiye
@app.event("app_mention")
def handle_mentions(event, say):
    user_text = event.get('text', '')
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_text)
    say(response.text)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()