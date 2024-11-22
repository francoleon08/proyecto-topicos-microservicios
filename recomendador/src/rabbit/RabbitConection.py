from ..service.ServiceRecommender import process_recommendation
from ..movies.UtilsMovies import fetch_movie_by_id, get_id_from_movie
from dotenv import load_dotenv
import pika
import os
import json

load_dotenv()

rabbitmq_host = os.getenv('RABBITMQ_HOST')
queue_movies = os.getenv('QUEUE_MOVIES')
queue_recommendations = os.getenv('QUEUE_RECOMMENDATIONS')
limit_movies = int(os.getenv('LIMIT_MOVIES'))

connection = None

movies_buffer = []

def init_connection():    
    global connection
    connection = connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_movies, durable=True)
    channel.queue_declare(queue=queue_recommendations, durable=True)
    print(f"Conectado a las colas: {queue_movies} y {queue_recommendations}")
    return channel

def close_connection():
    global connection
    if connection:
        connection.close()
        print("Conexión cerrada")
    
def consume_movies(channel):    
    channel.basic_consume(queue=queue_movies, on_message_callback=callback_movies, auto_ack=True)
    channel.start_consuming()

def callback_movies(ch, method, properties, body):    
    global movies_buffer
    
    process_movie(body)
    
    if len(movies_buffer) >= limit_movies:        
        recomendation = process_recommendation(movies_buffer)
        print(recomendation)
        #send_recomendation(ch, recomendation)
        movies_buffer.clear()        

def process_movie(body):
    global movies_buffer
    
    id_movie = get_id_from_movie(json.loads(body))
    movie = fetch_movie_by_id(id_movie)   
    movies_buffer.append(movie)

def send_recomendation(channel, message):    
    message_json = json.dumps(message)
    channel.basic_publish(
        exchange='',
        routing_key=queue_recommendations,
        body=message_json,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )    
