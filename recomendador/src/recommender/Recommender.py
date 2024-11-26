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

URL_MOVIES = f"{os.getenv('URL_MOVIES')}/movies/random?limit=1000"

def clean(clean):
    if not clean or not isinstance(clean, list):
        return ""
    return ', '.join(str(i.lower().replace(" ", "")) for i in clean)

def query_random_movie_endpoint(limit=1):
    try:
        #base_url = os.getenv('URL_MOVIES')  
        #url = f"{base_url}/movies/random?limit={limit}"
        response = requests.get(URL_MOVIES)
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
        url = f"http://localhost:3000/movies/filter?limit={limit}"#&timestamp={int(time.time())}
        headers = {"Content-Type": "application/json"}
        current_filters = filters.copy()  
        
        filter_removal_priority = ['languages', 'directors', 'cast', 'genres']
        
        while current_filters:
            response = requests.post(URL_MOVIES, json=current_filters, headers=headers)
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
    
def query_filter(filters, limit=1000):
    try:
        # Define the URL and headers
        url = f"http://localhost:3000/movies/filter?limit={limit}"#&timestamp={int(time.time())}
        headers = {"Content-Type": "application/json"}

        # Priority for removing filters
        filter_removal_priority = ["language", "director", "cast", "genre"]

        # Initialize variables
        best_movie = None
        best_match_score = 0
        current_filters = filters.copy()  # Start with all filters intact

        while current_filters:
            # Create the query payload by removing the prefix from each filter value
            query_payload = {
                key: value.split(":", 1)[1]  # Extract the value after the first colon
                for key, value in current_filters.items()
            }

            print(f"Trying with filters: {query_payload}")  # Debugging log

            # Send the request to the endpoint
            response = requests.post(URL_MOVIES, json=query_payload, headers=headers)
            response.raise_for_status()
            movies = response.json()

            if movies:
                for movie in movies:
                    # Calculate match score based on how many filters the movie satisfies
                    match_score = sum(
                        query_payload.get(key, "").lower() in str(movie.get(key, "")).lower()
                        for key in query_payload
                    )

                    # Update the best movie if this one has a higher score or rating
                    imdb_rating = float(movie.get("imdb", {}).get("rating", 0) or 0)
                    if (match_score > best_match_score) or (
                        match_score == best_match_score and imdb_rating > float(best_movie.get("imdb", {}).get("rating", 0) or 0)
                    ):
                        best_movie = movie
                        best_match_score = match_score

                # Stop searching if a movie matches all filters
                if best_match_score == len(query_payload):
                    return {"best_movie": best_movie, "best_filters": current_filters}

            # If no movies match or no perfect match found, remove the least critical filter
            if len(current_filters) > 1:
                for filter_key in filter_removal_priority:
                    if filter_key in current_filters:
                        del current_filters[filter_key]
                        break
            else:
                break

        # Return the best movie found, or None if no matches
        return {"best_movie": best_movie, "best_filters": current_filters if best_movie else {}}

    except Exception as e:
        print(f"Error querying filter endpoint with filters '{filters}': {e}")
        return {"best_movie": None, "best_filters": None}
    
def get_best_rated_movie_from_url(filters, limit=1):
    try:
        base_url = os.getenv('URL_MOVIES') 
        url = f"{base_url}/movies/random?limit={limit}"
        headers = {"Content-Type": "application/json"}

        # Sending the filters directly to the backend service
        response = requests.post(url, json=filters, headers=headers)
        response.raise_for_status()

        movies = response.json()

        if movies:
            filtered_movies = [movie for movie in movies if movie.get('imdb', {}).get('rating', 0) > 0]

            best_movie = max(filtered_movies, key=lambda x: x['imdb']['rating'])

            return best_movie
        else:
            print("No movies found after applying filters.")
            return None
    except Exception as e:
        print(f"Error fetching best-rated movie: {e}")
        return None

    best_movie = find_best_movie(filters)
    if best_movie:
        return best_movie

    reduced_filters = filters.copy()
    for key in list(reduced_filters.keys()):
        reduced_filters.pop(key)
        best_movie = find_best_movie(reduced_filters)
        if best_movie:
            return best_movie

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

def extract_movie_details(filters):
    cast_list = filters.get("cast", [])
    directors_list = filters.get("directors", [])
    genres_list = filters.get("genres", [])
    languages_list = filters.get("languages", [])

    predominant_cast = Counter(cast_list).most_common(1)[0][0] if cast_list else None
    predominant_director = Counter(directors_list).most_common(1)[0][0] if directors_list else None
    predominant_genre = Counter(genres_list).most_common(1)[0][0] if genres_list else None
    predominant_language = Counter(languages_list).most_common(1)[0][0] if languages_list else None

    return {
        "genre": predominant_genre,
        "cast": predominant_cast,
        "director": predominant_director,
        "language": predominant_language
    }
    
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
    
    best_filters = extract_movie_details(filters)
    
    #return best_filters
    
    #best_movie = query_filter_endpoint(best_filters)
    
    #best_movie = query_filter(best_filters)
    
    best_movie = get_best_rated_movie_from_url(best_filters, limit=1)

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