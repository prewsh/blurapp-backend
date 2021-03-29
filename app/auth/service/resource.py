from random import randint
from expiringdict import ExpiringDict
from app import  db
from app.auth.util import pil_image_to_base64
import pyqrcode ,json
import png 
from pyqrcode import QRCode



verify_expire_code = ExpiringDict(max_len=50, max_age_seconds=600) 

def random_gentarted(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def formate_number(number): 
    return ("{:,}".format(number)) 

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def sms_token(to,msg):
    url = "https://api.appmartgroup.com/v3/sms/postSend"
  
    headers = {
    'Content-Type': 'application/json',
    'apiKey': 'T58C6WXxkxibslDnAjk6',
    'Accept': 'application/json',
    'Connection': 'Keep-Alive',
    }
  
    payload = "{\n\t\"to\": \""+to+"\",\n    \"from\": \"VERIPAY\",\n    \"vendor_code\": \"7075365398\",\n    \"msg\": \""+msg+"\"\n}"
    try:
        response = requests.request("POST",url, headers=headers,data=payload)
    except ValueError:
          return False

    return response


#Generate Barcode 
def generate_barcode(qr_name):
    if not qr_name:
        return  "Qr Name is required" 
    # Generate QR code 
    url = pyqrcode.create(qr_name) 
    
    url.png("qrcodes/"+qr_name+".png", scale = 6)
    png=pil_image_to_base64("qrcodes/"+qr_name+".png")
    return  png







    