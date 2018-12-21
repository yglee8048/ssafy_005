from bs4 import BeautifulSoup as bs
import requests
import time

def get_theme_infos(store_num):
    url = 'http://www.master-key.co.kr/booking/booking_list_new'
    params = {"date" : time.strftime("%Y-%m-%d"), "store": store_num, "room" : ''}
    response = requests.post(url, params).text
    document = bs(response, 'html.parser')
    
    ul = document.select('.reserve')
    lis = document.select('.escape_view')
    
    themes = []
    for li in lis:
        theme = {
            'theme_name' : li.select('p')[0].text,
            'theme_type' : li.select('span')[0].text[7:],
            'fixednum' : li.select('span')[2].text[5:],
            'reservation' : []
        }
        for col in li.select('.col'):
            theme['reservation'].append({"time" : col.select_one('.time').text, "status" : col.select_one('.state').text})
        themes.append(theme)

    return themes


def masterkey():
    url = 'http://www.master-key.co.kr/home/office'
    response = requests.get(url).text
    document = bs(response, 'html.parser')
    
    # class 이므로 .을 붙여준다. id는 #을 붙여준다.
    ul = document.select('.escape_list')
    lis = document.select('.escape_view')
    
    base = 'http://www.master-key.co.kr'
    cafes = []
    for li in lis:
        cafe ={
            'title' : li.select('p')[0].text.replace('NEW', ''),
            'address' : li.select('dd')[0].text,
            'tel' : li.select('dd')[1].text,
            'link' : base + li.select('a')[0].get('href')
        }
        # if cafe['title'].endwith('NEW') : cafe['title'] = cafe['title'][:-3]
        cafe['themes'] = get_theme_infos(int(cafe['link'][cafe['link'].find('bid=')+4:]))
        cafes.append(cafe)
    return cafes

        
def get_msg(msg):
    cafes = masterkey()
        
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
    
    return msg