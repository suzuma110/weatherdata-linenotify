import requests
import os


def send_line_notify(message):
    """
    LINEに通知する
    """
    # Put your token
    line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    payload = {'message': message}
    files = {"imageFile": open(
        'screen.png', 'rb')}
    requests.post(line_notify_api, headers=headers,
                  params=payload, files=files)
    print("LINE Notifyへ送信しました。")

