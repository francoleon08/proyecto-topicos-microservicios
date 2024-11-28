from flask import Flask
from .rabbit.RabbitConection import init_connection, consume_movies

app = Flask(__name__)

channel = init_connection()
consume_movies(channel)