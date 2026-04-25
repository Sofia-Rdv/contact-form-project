from flask import Flask
import logging
from logging_module.my_logger_config import setup_logging

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" # нужно для работы flask-сообщений
from app import routes
setup_logging()