import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import google.generativeai as genai

load_dotenv()

# Slack Bot
app = App(token=os.environ["SLACK_TOKEN"])

# Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

@app.event("app_mention")
def handle_mentions(event, say):

    try:
        user_text = event.get("text", "")

        # Remove the bot mention
        if ">" in user_text:
            user_text = user_text.split(">", 1)[1].strip()

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(user_text)

        say(response.text)

    except Exception as e:
     if "429" in str(e):
        say("API rate limit exceeded.please try again after 15 seconds.")
    else:
        say(f"Error: {str(e)}")

if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    ).start()