import webbrowser
from collections import Counter
from urllib.request import urlopen, quote
import json
import requests
import itchat
from itchat.content import *

def getlnglat(address):
    '''
    返回字典形式的城市经纬度和其他信息数据
    '''
    address = quote(address)
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'Uba11lIVgQGGj2xPZPif4mfRtNXjVhSo'
    uri = url + '?output=' + output + '&address=' + address + '&ak=' + ak
    temp = urlopen(uri)
    temp = json.loads(temp.read().decode())
    return temp

@itchat.msg_register(itchat.content.TEXT)
def address_reply(msg):
    if(msg['Text']=="address"):
        source = msg['FromUserName']
        address = itchat.get_friends(update=False)
        print(type(address))
        address_list = ''
        address_json = dict()
        address_city_list = []
        for i in address:
            nickname = i["NickName"]
            city = i["City"]
            province = i["Province"]
            address_i = nickname + ':' + province + ' ' + city
            address_list += address_i + '\n'
            city_json = getlnglat(city) #type: <class 'dict'>
            if city_json['status'] == 0:
                address_city_list.append(city)
                print(city_json)
                address_json[city] = city_json
            elif city_json['status'] != 0:
                province_json = getlnglat(province) #type: <class 'dict'>
                if province_json['status'] == 0:
                    address_city_list.append(province)
                    print(province_json)
                    address_json[province] = province_json
        
        webbrowser.open('/home/tiger/Workspace/itChatAttendanceCheck/addressMap/index.html')
        print(address_json)
        itchat.send(address_list, source)

itchat.auto_login(hotReload=True)
itchat.run()