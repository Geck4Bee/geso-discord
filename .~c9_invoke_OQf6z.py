import sys
sys.path.append('lib')

import requests
import os
import json
import datetime

def sendWebHook(content):
    try:
        print('shot webhook!')
        response = requests.post(
            os.environ['WEBHOOK'],
            json.dumps({"content": content}),
            headers={'Content-Type': 'application/json'}
        )
        print(response)
    except Exception as ew:
        sys.stderr.write("*** error *** in SendWebHook ***\n")
        sys.stderr.write(str(ew) + "\n")
    else:
        return response

def handler(event, context):
    content = '●GESONTACLE更新\n'
    response = 'start'
    flagSendWebhook = False
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            #項目が追加された時の処理
            newItem = record['dynamodb']['NewImage']
            dt = datetime.datetime.fromisoformat(newItem['updatedAt']['S'])
            content += '<新着>\n' + newItem['title']['S'] + ': ' + dt.strftime("%Y/%m/%d %H:%M:%S") +'\n' + 'https://gesontacle.com/post/' + newItem['id']['S'] + '\n'
            flagSendWebhook = True
        elif record['eventName'] == 'MODIFY':
            #項目が変更された時の処理
            oldItem = record['dynamodb']['OldImage']
            newItem = record['dynamodb']['NewImage']
            dt = datetime.datetime.fromisoformat(newItem['updatedAt']['S'])
            content += '<更新>\n' + newItem['title']['S'] + ': ' + dt.strftime("%Y/%m/%d %H:%M:%S") +'\n' + 'https://gesontacle.com/post/' + newItem['id']['S'] + '\n'
            flagSendWebhook = True
        elif record['eventName'] == 'REMOVE':
            #項目が削除された時の処理
            deletedItem = record['dynamodb']['OldImage']
    if flagSendWebhook:
        response = sendWebHook(content)
    data = {
        'output': 'Hello World',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'response': response
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
