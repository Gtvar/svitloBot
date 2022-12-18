import json
import os
import requests

def telegram_bot_sendtext(botChatID, botMessage):

   botToken = os.environ['BOT_TOKEN']
   url = 'https://api.telegram.org/bot' + botToken + '/sendMessage?chat_id=' + botChatID + '&parse_mode=Markdown&text=' + botMessage
   response = requests.get(url)

   return response.json()

def lambda_handler(event, context):

    botChatID = event['botChatID']
    botMessage = event['botMessage']
    telegram_bot_sendtext(botChatID, botMessage)

    return {
        'statusCode': 200,
    }
