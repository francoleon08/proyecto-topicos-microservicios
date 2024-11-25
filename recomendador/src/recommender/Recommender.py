import pandas as pd
import numpy as np
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
from dotenv import load_dotenv
import os
import warnings
import time
import re

warnings.filterwarnings('ignore')
load_dotenv()

URL_MOVIES = os.getenv('URL_MOVIES')

def clean_genres(genres):
    if not genres:
        return ""
    return ', '.join(str(i.lower().replace(" ", "")) for i in genres)

def query_random_movie_endpoint(limit=1):
    try:
        #url = f"http://localhost:3000/movies/random?limit={limit}"
        url = f"http://localhost:3000/movies/filter?limit={limit}&timestamp={int(time.time())}"
        response = requests.get(url)
        response.raise_for_status()
        movies = response.json()

        if movies:
            return movies[0]  
        return None
    except Exception as e:
        print(f"Error querying random movie endpoint: {e}")
        return None

def query_filter_endpoint(filters, limit=1000):
    try:
        #url = URL_MOVIES + f"/movies/filter?limit={limit}"
        url = f"http://localhost:3000/movies/filter?limit={limit}&timestamp={int(time.time())}"
        headers = {"Content-Type": "application/json"}
        current_filters = filters.copy()  
        
        filter_removal_priority = ['languages', 'directors', 'cast', 'genres']
        
        while current_filters:
            response = requests.post(url, json=current_filters, headers=headers)
            response.raise_for_status()
            movies = response.json()

            if movies: 
                return max(movies, key=lambda x: float(x.get('imdb', {}).get('rating', 0) or 0))

            if len(current_filters) > 1: 
                for filter_key in filter_removal_priority:
                    if filter_key in current_filters:
                        del current_filters[filter_key]
                        break
            else:
                break 

        return None 
    except Exception as e:
        print(f"Error querying filter endpoint with filters '{filters}': {e}")
        return None

def extract_predominant(movies):
    """
    Extracts the predominant values for the predefined fields from the movies data.
    Fields include: genres, cast, directors, and languages.
    
    :param movies: List of dictionaries representing movies.
    :return: Dictionary of predominant values for predefined fields.
    """
    # Constant fields to process
    fields = ["genres", "cast", "directors", "languages"]
    
    results = {}
    
    for field in fields:
        field_counter = Counter()
        
        # Loop through each movie and process the field
        for movie in movies:
            field_data = movie.get(field, None)
            
            # Handle lists (e.g., genres, cast) or single values (e.g., language, directors)
            if isinstance(field_data, list):
                # Remove prefix like 'genre:', 'cast:', etc. and count the actual values
                field_counter.update([item.split(':')[-1].lower() for item in field_data if item])  # Get value after ':' and lowercase
            elif field_data:  # Single values
                field_counter.update([field_data.lower()])
        
        # Find the most common value(s) for the field
        most_common = field_counter.most_common(1)  # Get the top result
        results[field] = most_common[0][0] if most_common else None  # Return top or None if empty
    
    return results

def extract_movie_details(soup_list):
    movie_details = []

    # Iterate through the soup list
    for entry in soup_list:
        entry = entry.strip()
        
        # Regular expressions to extract each component
        title_match = re.match(r"^(.*?) genre:", entry)
        genre_match = re.findall(r"genre:([^ ]+)", entry)
        cast_match = re.findall(r"cast:([^,]+(?:, [^,]+)*)", entry)
        directors_match = re.findall(r"directors:([^,]+(?:, [^,]+)*)", entry)
        languages_match = re.findall(r"languages:([^,]+(?:, [^,]+)*)", entry)


        # Extract and clean the components
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        genres = ', '.join(genre_match)
        cast = ', '.join(cast_match)
        directors = ', '.join(directors_match)
        languages = ', '.join(languages_match)

        # Append the details to the result list
        movie_details.append({
            'title': title,
            'genres': genres,
            'cast': cast,
            'directors': directors,
            'languages': languages
        })
    
    return movie_details

def process_recommendations(movie_history_data):
    movie_history = pd.DataFrame(movie_history_data)              

    movie_history['genres_clean'] = movie_history['genres'].apply(clean_genres)
    genres_list = movie_history['genres_clean'].apply(lambda x: x.split(', ')).tolist()
    cast_list = movie_history['cast'].apply(lambda x: x.split(', ') if isinstance(x, str) else []).tolist()
    directors_list = movie_history['directors'].apply(lambda x: x.split(', ') if isinstance(x, str) else []).tolist()
    languages_list = movie_history['languages'].apply(lambda x: x.split(', ') if isinstance(x, str) else []).tolist()

    movie_history['soup'] = movie_history.apply(
        lambda x: ' '.join([
            str(x['title']),
            ' '.join([f"genre:{genre}" for genre in genres_list[x.name] if genre]),  # Access genres list directly
            ' '.join([f"cast:{member}" for member in cast_list[x.name] if member]),  # Access cast list directly
            ' '.join([f"director:{director}" for director in directors_list[x.name] if director]),  # Access directors list directly
            ' '.join([f"language:{lang}" for lang in languages_list[x.name] if lang])  # Access languages list directly
        ]),
        axis=1
    )
    
    #return movie_history['soup'].tolist()      #TEST DONDE ANDA
    
    movie_details = extract_movie_details(movie_history['soup'])
    
    return movie_details
    
    #predominant_features = movie_history['soup'].apply(extract_predominant_from_soup) #aca se rompe
    
    predominant_features = extract_predominant(movie_history_data['soup'].tolist())

    predominant_genres, predominant_cast, predominant_directors, predominant_languages = zip(*predominant_features)

    #filters = {
    #    "genres": predominant_genres,
    #    "cast": predominant_cast,
    #    "directors": predominant_directors,
    #    "languages": predominant_languages
    #}

    filters = {
        'genres': tuple(g for g in predominant_genres if g),
        'cast': tuple(c for c in predominant_cast if c),
        'directors': tuple(d for d in predominant_directors if d),
        'languages': tuple(l for l in predominant_languages if l),
    }
    
    return filters
    
    best_movie = query_filter_endpoint(filters)
    
    if best_movie:
        return {
            "source_movies": movie_history['title'].tolist(), 
            "recommended_movie_best": {
                "imdb": best_movie.get("imdb"),
                "title": best_movie.get("title"),
                "poster": best_movie.get("poster"),
                "plot": best_movie.get("plot"),
                "genres": best_movie.get("genres"),  
                "year": best_movie.get("year")
            }
        }

    random_movie = query_random_movie_endpoint(limit=1)
    
    return {
        "source_movies": movie_history['title'].tolist(),
        "recommended_movie_random": {
            "imdb": random_movie.get("imdb"),
            "title": random_movie.get("title"),
            "poster": random_movie.get("poster"),
            "plot": random_movie.get("plot"),
            "genres": random_movie.get("genres"),
            "year": random_movie.get("year")  
        }
    }