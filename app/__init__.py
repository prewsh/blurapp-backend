from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS, cross_origin

db = SQLAlchemy()
ma = Marshmallow()
 
def create_app(config_filename):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_filename)
    
    from app.auth import app_service
    #from app.chat import chat_service
    from app.wallet import wallet_service
    app.register_blueprint(app_service, url_prefix='/api')
    app.register_blueprint(wallet_service, url_prefix='/wallet')
    # app.register_blueprint(chat_service, url_prefix='/chat')
  

    db.init_app(app)

    return app