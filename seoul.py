import requests
import json
import time

def seoul():

    url = 'http://www.seoul-escape.com/reservation/change_date/'
    params = {
        'current_date' : time.strftime('%Y/%m/%d')
    }
    
    response = requests.get(url, params = params).text
    document = json.loads(response)
    
    dic = {}
    arr = list(range(12))
    arr[1] = '강남1호점'
    arr[3] = '홍대1호점'
    arr[4] = '부산 서면점'
    arr[5] = '인천 부평점'
    arr[10] = '강남 2호점'
    arr[11] = '홍대 2호점'
    
    # dic = { '카페이름' : { '방이름' : [ {시간, 예약여부}, ... ] } }
    
    for x in document['gameRoomList']:
        dic[arr[x['branch_id']]] = {}
        
    for x in document['gameRoomList']:
        dic[arr[x['branch_id']]][x['room_name']] = []
        
    for x in document['bookList']:
        dic[arr[x['branch_id']]][x['room']].append({'time' : x['hour'], 'is_booked' : x['booked']})
    
    return dic
    
    
def get_msg(msg):
    dic = seoul()
    # dic = { '카페이름' : {'방이름' : [{시간, 예약여부}]} }
    #'time' : x['hour'], 'is_booked' : x['booked']
    
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
                    if(z['is_booked']) : msg += "예약완료\n"
                    else : msg += "예약가능\n"
        else :
            msg = '잘못된 지점명입니다.\n'
            msg += '지점명은 다음과 같습니다.\n'
            msg += '\n'.join(dic.keys())
    
    return msg