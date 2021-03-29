import os
import jwt,json,secrets,datetime,uuid,requests
from twilio.rest import Client

auth_token =""
account_sid =""
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


