#!/usr/bin/python

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Case/")

activate_this = '/var/www/Case/Case/Pyserver/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
from Case import create_app as application
application.secret_key = '0307beb835b20ea53845e3230a7d8d6907dcc5957546580e044c846065da0bd7'

