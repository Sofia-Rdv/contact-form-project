from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" # нужно для работы flask-сообщений
from app import routes