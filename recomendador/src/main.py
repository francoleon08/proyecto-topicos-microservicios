from flask import Flask
from .rabbit import RabbitConection

app = Flask(__name__)

channel = RabbitConection.init_connection()
RabbitConection.consume_movies(channel)