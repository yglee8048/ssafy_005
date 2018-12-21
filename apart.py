import requests
import json


def apart():
    url = 'http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=B&p_apt_code=439302&p_house_cd=1&p_acc_year=2017&areaCode=&priceCode='
    
    headers = {
        "Host": "rt.molit.go.kr",
        "Referer": "http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND"
    }
    
    response = requests.get(url, headers = headers).text
    document = json.loads(response)
    
    apartInfo = []
    
    for apart in document['result']:
        apartInfo.append({
                "location" : apart["JIBUN_NAME"],
                "apart_name" : apart["BLDG_NM"],
                "apart_size" : apart["BLDG_AREA"],
                "apart_cost" : apart["SUM_AMT"],
                "month" : apart["DEAL_MM"],
                "date" : apart["DEAL_DD"]
                })
    return apartInfo