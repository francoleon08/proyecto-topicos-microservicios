import pika
import requests
import json

RABBITMQ_URL = 'amqp://rabbitmq:5672'
MOVIES_QUEUE = 'movies'
RECOMMENDATIONS_QUEUE = 'recommendation'

def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=RECOMMENDATIONS_QUEUE, durable=True)
    return channel

def fetch_movie_history_from_queue():
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=MOVIES_QUEUE, durable=True)

        method_frame, header_frame, body = channel.basic_get(queue=MOVIES_QUEUE)
        if body:
            movie_history = json.loads(body)
            print(f"Received movie history from queue: {movie_history}")
            channel.basic_ack(method_frame.delivery_tag)
            return movie_history
        else:
            print("No message received from the movies queue")
            return []
    except Exception as e:
        print(f"Error fetching movie history from queue: {e}")
        return []

def send_recommendations_to_rabbitmq(recommendation):
    try:
        channel = get_rabbitmq_channel()
        result_message = json.dumps({
            'recommendation': recommendation
        })
        channel.basic_publish(
            exchange='',
            routing_key=RECOMMENDATIONS_QUEUE,
            body=result_message,
            properties=pika.BasicProperties(
                delivery_mode=2  
            )
        )
        print("Sent recommendation to RECOMMENDATIONS_QUEUE")
    except Exception as e:
        print(f"Error sending recommendations to RabbitMQ: {e}")
        raise