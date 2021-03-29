import os
import jwt,json,secrets,datetime,uuid,requests
from twilio.rest import Client

auth_token ="7ae1ebc581cf62d14faa65c7321158d4"
account_sid ="ACc50496b3b6c408b88ff1cbabbd2fc47c"
phone="+18478606711"





def SendSMSNg(to,code):

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body='[PAYSCRIN]Verification code:'+code+ ' .Do not share this code with anyone',
            from_=phone,
            to='+234'+to
        )
    
    print(message.sid)


