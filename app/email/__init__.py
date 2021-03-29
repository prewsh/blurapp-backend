import os
import jwt,json,secrets,datetime,uuid,requests


auth_token =""





#function in use
def send_simple_message(to,subject,sender,message):
    res= requests.post(
        "https://api.mailgun.net/v3/info.pixufy.com/messages",
        auth=("api", auth_token),
        data={"from": sender+"<noreply@info.pixufy.com>",
              "to": to,
              "subject": subject,
              "text": message,
               "html": message
              })
    return res.json()


def send_complex_message():
    return requests.post(
        "https://api.mailgun.net/v3/info.pixufy.com/messages",
        auth=("api", "YOUR_API_KEY"),
        files=[("attachment", ("test.jpg", open("files/test.jpg","rb").read())),
               ("attachment", ("test.txt", open("files/test.txt","rb").read()))],
        data={"from": "Excited User <YOU@YOUR_DOMAIN_NAME>",
              "to": "foo@example.com",
              "cc": "baz@example.com",
              "bcc": "bar@example.com",
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!",
              "html": "<html>HTML version of the body</html>"})