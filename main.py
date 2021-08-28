from gmail_service import GmailService
from slack_notifer import SlackNotifer
import json
import textwrap

def run():
    messages = GmailService().get_messages()
    
    # 未読メッセージが無い場合は終了
    if messages is None:
        print('未読のメッセージはありません。')
        
        return
    
    # 未読メッセージがある場合はSlack通知を送信
    for message in json.loads(messages):
        heredoc =  textwrap.dedent('''
            ```
            ☆ 未読のメッセージがあります。☆
            
            日付: {date}
            差出人: {_from}
            件名: {subject}
            本文: {snippet}

            続きはこちら → https://mail.google.com/mail/u/0/#label/unread/{id}
            ```
        ''').format(
            date = message['date'],
            _from = message['from'],
            subject = message['subject'],
            snippet = message['snippet'],
            id = message['id']
        )
        
        print('Slack通知を送信中...')

        SlackNotifer().send(heredoc)

if __name__ == '__main__':
    run()
