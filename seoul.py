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
    
    for x in document['gameRoomList']:
        dic[arr[x['branch_id']]] = {}
        
    for x in document['gameRoomList']:
        dic[arr[x['branch_id']]][x['room_name']] = []
        
    for x in document['bookList']:
        dic[arr[x['branch_id']]][x['room']].append({'time' : x['hour'], 'is_open' : x['booked']})
    
    return dic
    
    # dic = { '카페이름' : {'방이름' : [{시간, 예약여부}]} }