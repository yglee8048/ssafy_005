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
        cafes = masterkey.masterkey()
        
        if(msg == "마스터키"):
            msg = '해당 카페의 예약 정보를 확인하고 싶다면 마스터키 (지점이름)을 입력하세요. ex)마스터키 부천점 \n'
            for cafe in cafes:
                msg += cafe['title'] + '\n' + cafe['address'] + '\n' + cafe['tel'] + '\n' + cafe['link'] + '\n'
        else:
            msg = msg.split(' ')[1]
            ck = False
            for cafe in cafes:
                if(cafe['title'] == msg):
                    ck = True
                    msg = cafe['title'] + '\n' + cafe['address'] + '\n' + cafe['tel'] + '\n' + cafe['link'] + '\n'
                    for x in cafe['themes']:
                        msg += '***** ' + x['theme_name'] + ' / ' + x['theme_type'] + '타입 / 정원 : ' + x['fixednum'] + ' *****\n'
                        for y in x['reservation']:
                            msg += y['time'] + ' // ' + y['status'] + '\n'
            if(not ck):
                msg = "존재하지 않는 지점입니다."
    
    if(msg.startswith("서울이스케이프")):
        dic = seoul.seoul()
        # dic = { '카페이름' : {'방이름' : [{시간, 예약여부}]} }
        #'time' : x['hour'], 'is_open' : x['booked']
        
        if(msg == '서울이스케이프'):
            msg = '서울이스케이프 (지점명) 을 입력해주세요.\n'
            msg += '지점명은 다음과 같습니다.\n'
            msg += '\n'.join(dic.keys())
        else:
            cafe_name = msg.split(' ')[1]
            if(cafe_name in dic.keys()):
                msg += "\n"
                for y in list(dic[cafe_name].keys()):
                    # y = '방이름'
                    msg += y + '*******\n'
                    for z in dic[cafe_name][y]:
                        # z = {시간, 예약여부}
                        msg += z['time'] + " "
                        if(z['is_open']) : msg += "예약완료\n"
                        else : msg += "예약가능\n"
            else :
                msg = '잘못된 지점명입니다.\n'
                msg += '지점명은 다음과 같습니다.\n'
                msg += '\n'.join(dic.keys())
    
    elif(msg == '아파트'):
        apartInfo = apart.apart()
        msg = ''
        for a in apartInfo:
            msg += a['location'] + '\n'
            msg += a['apart_name'] + '\n'
            msg += str(a['apart_size']) + '\n'
            msg += str(a['apart_cost']) + '\n'
    else :
        msg = '등록되지 않은 명령입니다.'
    
    url = telegram_url + '/bot{}/sendMessage'.format(telegram_token)
    requests.get(url, params ={"chat_id" : chat_id, "text" : msg})
    
    return '', 200

