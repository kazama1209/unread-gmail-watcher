import os
from slack_sdk import WebClient
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN') # トークン
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')     # 送信先のチャンネル

class SlackNotifer:
    def __init__(self):
        self.slack_bot_token = SLACK_BOT_TOKEN
        self.slack_channel = SLACK_CHANNEL
        self.client = WebClient(token = self.slack_bot_token)
    
    def send(self, text):
        self.client.chat_postMessage(
            channel = self.slack_channel,
            text = text,
            as_user = True
        )
