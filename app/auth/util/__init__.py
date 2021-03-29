
from random import randint
from PIL import Image
from io import BytesIO
import base64,os
from app import  db



def pil_image_to_base64(path):
    with open(path, "rb") as image_file:
     encoded_string = base64.b64encode(image_file.read()).decode('ascii')
     return encoded_string


def base64_to_pil_image(base64_img):
    return Image.open(BytesIO(base64.b64decode(base64_img)))


def makDir(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")

def random_gentarted(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
    
def save_changes(data):
    db.session.add(data)
    db.session.commit()

def send_email():
   return True