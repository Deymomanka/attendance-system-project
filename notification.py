import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


def send_slack_notification(name, status):
    """
    Slackに通知を送信する関数
    :param webhook_url: SlackのWebhook URL
    :param name: ユーザー名
    :param status: ステータス（出席、欠席など）
    :param now: 現在の日時
    """

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("SlackのWebhook URLが設定されていません。")
        return

    message = {
        "text": f"{name}さんが, {status}しました（顔認証打刻）"
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(message), headers=headers)

    if response.status_code != 200:
        print(f"Slack通知に失敗しました: {response.status_code}, {response.text}")
    else:
        print(f"Slack通知成功")


        
    
