import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from apps import db
from apps.product.models import ProductFavorite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Gesoft9919.@101.126.90.255:63306/liandong21mall?charset=utf8mb4&use_unicode=1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.create_all()
    print('ProductFavorite table created successfully')
