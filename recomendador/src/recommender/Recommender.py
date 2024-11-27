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
import json

warnings.filterwarnings('ignore')
load_dotenv()

URL_MOVIES = os.getenv('URL_MOVIES')

def clean(clean):
    if not clean or not isinstance(clean, list):
        return ""
    return ', '.join(str(i.lower().replace(" ", "")) for i in clean)

def query_random_movie_endpoint(limit=1):
    try:
        url = f"{URL_MOVIES}/movies/random?limit={limit}"
        response = requests.get(url)
        response.raise_for_status()
        movies = response.json()

        if movies:
            return movies[0]  
        return None
    except Exception as e:
        print(f"Error querying random movie endpoint: {e}")
        return None

def query_filter_endpoint(best_genre_json, best_cast_json, best_director_json, best_language_json):
    try:
        limit=1000
        url = f"{URL_MOVIES}/movies/filter?limit={limit}" 
        headers = {"Content-Type": "application/json"}
    
        response_genre = requests.post(url, body=best_genre_json, headers=headers)
        response_genre.raise_for_status()  
        movies_genre = set(response_genre.json())
        
        response_cast = requests.post(url, body=best_cast_json, headers=headers)
        response_cast.raise_for_status()  
        movies_cast = set(response_cast.json())
        
        response_director = requests.post(url, body=best_director_json, headers=headers)
        response_director.raise_for_status()  
        movies_director = set(response_director.json())
        
        response_language = requests.post(url, body=best_language_json, headers=headers)
        response_language.raise_for_status()  
        movies_language = set(response_language.json())
        
        top_movies = movies_genre.intersection(movies_cast.intersection(movies_director.intersection(movies_language)))

        if top_movies: 
            best_movie = max(top_movies, key=lambda x: float(x.get('imdb', {}).get('rating', 0) or 0))
            return best_movie
        else:
            top_movies = movies_genre.intersection(movies_cast.intersection(movies_director))
            if top_movies:
                best_movie = max(top_movies, key=lambda x: float(x.get('imdb', {}).get('rating', 0) or 0))
                return best_movie
            else:
                top_movies = movies_genre.intersection(movies_cast)
                if top_movies:
                    best_movie = max(top_movies, key=lambda x: float(x.get('imdb', {}).get('rating', 0) or 0))
                    return best_movie

        return None  
    
    except Exception as e:
        print(f"Error querying filter endpoint with filters")
        return None

def extract_predominant_from_soup(soup):
    tokens = soup.split()
    token_counts = Counter(tokens)

    genre_counts = Counter([token for token in tokens if token.startswith("genre:")])
    cast_counts = Counter([token for token in tokens if token.startswith("cast:")])
    director_counts = Counter([token for token in tokens if token.startswith("director:")])
    language_counts = Counter([token for token in tokens if token.startswith("language:")])

    predominant_genre = genre_counts.most_common(1)[0][0] if genre_counts else None
    predominant_cast = cast_counts.most_common(1)[0][0] if cast_counts else None
    predominant_director = director_counts.most_common(1)[0][0] if director_counts else None
    predominant_language = language_counts.most_common(1)[0][0] if language_counts else None

    return predominant_genre, predominant_cast, predominant_director, predominant_language

def extract_movie_details(filters, field):
    cast_list = filters.get("cast", [])
    directors_list = filters.get("directors", [])
    genres_list = filters.get("genres", [])
    languages_list = filters.get("languages", [])

    predominant_cast = Counter(cast_list).most_common(1)[0][0] if cast_list else None
    predominant_director = Counter(directors_list).most_common(1)[0][0] if directors_list else None
    predominant_genre = Counter(genres_list).most_common(1)[0][0] if genres_list else None
    predominant_language = Counter(languages_list).most_common(1)[0][0] if languages_list else None

    if field == 0:
        return predominant_genre
    
    if field == 1:
        return predominant_cast
    
    if field == 2:
        return predominant_director
    
    if field == 3:
        return predominant_language
    
def process_recommendations(movie_history_data):
    movie_history = pd.DataFrame(movie_history_data)              

    movie_history['genres_clean'] = movie_history['genres'].apply(clean)
    genres_list = movie_history['genres_clean'].apply(lambda x: x.split(', ')).tolist()
    
    movie_history['cast_clean'] = movie_history['cast'].apply(clean)
    cast_list = movie_history['cast_clean'].apply(lambda x: x.split(', ')).tolist()
    
    movie_history['directors_clean'] = movie_history['directors'].apply(clean)
    directors_list = movie_history['directors_clean'].apply(lambda x: x.split(', ')).tolist()
    
    movie_history['languages_clean'] = movie_history['languages'].apply(clean)
    languages_list = movie_history['languages_clean'].apply(lambda x: x.split(', ')).tolist()

    movie_history['soup'] = movie_history.apply(
        lambda x: ' '.join([
            str(x['title']),
            ' '.join([f"genre:{genre}" for genre in genres_list[x.name] if genre]),  
            ' '.join([f"cast:{member}" for member in cast_list[x.name] if member]),  
            ' '.join([f"director:{director}" for director in directors_list[x.name] if director]), 
            ' '.join([f"language:{lang}" for lang in languages_list[x.name] if lang])  
        ]),
        axis=1
    )
 
    predominant_features = movie_history['soup'].apply(extract_predominant_from_soup) 

    predominant_genres, predominant_cast, predominant_directors, predominant_languages = zip(*predominant_features)

    filters = {
        'genres': tuple(g for g in predominant_genres if g),
        'cast': tuple(c for c in predominant_cast if c),
        'directors': tuple(d for d in predominant_directors if d),
        'languages': tuple(l for l in predominant_languages if l),
    }

    best_genre = extract_movie_details(filters,0)
    best_genre_json = json.dumps(best_genre)
    
    best_cast = extract_movie_details(filters,1)
    best_cast_json = json.dumps(best_cast)
    
    best_directors = extract_movie_details(filters,2)
    best_director_json = json.dumps(best_directors)
    
    best_languages = extract_movie_details(filters,3)
    best_languages_json = json.dumps(best_languages)

    best_movie = query_filter_endpoint(best_genre_json,best_cast_json,best_director_json,best_languages_json)
    
    return best_movie

    #best_movie_based_on_genre = query_filter_endpoint(best_genre, limit=1000)
    
    #return best_movie_based_on_genre

    #best_filters = extract_movie_details(filters)
    
    #return best_filters
   
    #best_movie = query_filter_endpoint(best_filters, limit=1000)

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