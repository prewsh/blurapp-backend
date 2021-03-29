import os
import jwt,json,secrets,datetime,uuid,requests


token ="bot1178749669:AAEZUpb3Ni4udCVmAvb-6XCLXTUKpSAvB2A"
chat_id="-404256714"
payscrin_chat_id="-1001407075788"


def myNotifyBot(data):
    
    btc_url = "https://api.telegram.org/"+token+"/sendmessage?chat_id="+chat_id+"&text="+data+""
    response = requests.get(btc_url)
    res= response.json()

def myTalkBot(data):
    
    btc_url = "https://api.telegram.org/"+token+"/sendmessage?chat_id="+payscrin_chat_id+"&text="+data+""
    response = requests.get(btc_url)
    res= response.json()
