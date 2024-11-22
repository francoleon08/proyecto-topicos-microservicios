import requests
from dotenv import load_dotenv
import os

load_dotenv()
URL_MOVIES = os.getenv('URL_MOVIES')

def fetch_movie_by_id(id):
    try:
        url= URL_MOVIES + "/movies?id=" + str(id)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching movie with id '{id}': {e}")
        return None    
            
def get_id_from_movie(movie):
    return movie["imdb"]["id"]