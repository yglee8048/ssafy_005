from flask import Flask, render_template, request
import os
import requests
import masterkey, apart, seoul

app = Flask(__name__)
telegram_token = os.getenv('telegram_token')
telegram_url = 'https://api.hphk.io/telegram'

@app.route('/set_webhook')
def set_webhook():
    url = telegram_url + '/bot' + telegram_token + '/setWebhook'
    params = {
        'url' : "https://ssafy-week2-yglee8048.c9users.io/{}".format(telegram_token)
    }
    response = requests.get(url, params = params).text
    return response

@app.route('/{}'.format(os.getenv('telegram_token')), methods=['POST'])
def telegram() :
    # 텔레그램으로부터 요청이 들어 올 경우, 해당 요청을 처리하는 코드
    response = request.get_json()
    #print(response)
    '''
    {
    'update_id': 658018519,
    'message': {'message_id': 13, 
                'from': {'id': 735839461, 'is_bot': False, 'first_name': 'Q', 'last_name': 'Lee', 'language_code': 'ko'},
                'chat': {'id': 735839461, 'first_name': 'Q', 'last_name': 'Lee', 'type': 'private'},
                'date': 1545357272,
                'text': 'lksadndlka'
                }
    }
    '''
    # message를 발송한 사람
    chat_id = response['message']['from']['id']
    # message 내용
    msg = response['message']['text']
    
    if(msg.startswith("마스터키")):
        msg = masterkey.get_msg(msg)
    
    elif(msg.startswith("서울이스케이프")):
        msg = seoul.get_msg(msg)
    
    elif(msg == '아파트'):
        msg = apart.get_msg(msg)
        
    else :
        msg = '등록되지 않은 명령입니다.'
    
    url = telegram_url + '/bot{}/sendMessage'.format(telegram_token)
    requests.get(url, params ={"chat_id" : chat_id, "text" : msg})
    
    return '', 200

