import os
import json
import requests
import boto3

RESULT_NO = "no"
RESULT_YES = "yes"

def send_request():
    hostname = os.environ['HOSTNAME']

    try:
      response = requests.get(hostname, verify=False, timeout=1)
    except:
      return -1

    return response.status_code

def telegram_bot_sendtext(bot_message):

   client = boto3.client('lambda')

   bot_chatIDS = [item for item in os.environ['BOT_CHAT_IDS'].split(",") if item]
   for bot_chatID in bot_chatIDS:
        inputParams = {
            "botChatID": bot_chatID,
            "botMessage": bot_message
        }

        response = client.invoke(
            FunctionName = os.environ['TELEGRAM_FUNCTION_NAME'],
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )

        responseFromChild = json.load(response['Payload'])

   return responseFromChild

def svitlo_is_enabled():
    client = boto3.client('ssm')
    parameter = client.get_parameter(Name='svitlo.is_enabled', WithDecryption=False)

    return parameter ['Parameter']['Value']

def write_svitlo_param(value):
    client = boto3.client('ssm')
    client.put_parameter(
         Name='svitlo.is_enabled',
         Value=value,
         Type='String',
         Overwrite=True
       )

    return value


def get_text(result):
    if RESULT_YES == result:
        return 'Світло з\'явилося.😎 Слава Україні!🇺🇦'
    else:

        return 'Ой лишенько, світло зникло!🌃 Смерть москалям!😡'


def lambda_handler(event, context):
    is_enabled = svitlo_is_enabled()

    if send_request() == 200:
        result = RESULT_YES
    else:
        result = RESULT_NO

    if result == is_enabled:
        return 1

    write_svitlo_param(result)

    text = get_text(result)
    telegram_bot_sendtext(text)

    return text