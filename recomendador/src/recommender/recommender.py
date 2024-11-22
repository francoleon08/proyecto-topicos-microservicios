import pandas as pd
import numpy as np
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import warnings

warnings.filterwarnings('ignore')

def clean_genres(genres):
    return ', '.join(str.lower(i.replace(" ", "")) for i in genres.split(', '))

def query_filter_endpoint(filters, limit=1000):
    try:
        url = f"http://movies:3000/movies/filter?limit={limit}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=filters, headers=headers)
        response.raise_for_status()
        movies = response.json()

        if movies:
            return max(movies, key=lambda x: x.get('rating', 0)) 
        return None
    except Exception as e:
        print(f"Error querying filter endpoint with filters '{filters}': {e}")
        return None
    
def query_random_movie_endpoint(limit=1):
    try:
        url = f"http://movies:3000/movies/random?limit={limit}"
        response = requests.get(url)
        response.raise_for_status()
        movies = response.json()

        if movies:
            return movies[0]  
        return None
    except Exception as e:
        print(f"Error querying random movie endpoint: {e}")
        return None

def extract_predominant_from_soup(soup):
    tokens = soup.split()
    token_counts = Counter(tokens)

    predominant_genre = genre_counts.most_common(1)[0][0] if genre_counts else None
    predominant_cast = cast_counts.most_common(1)[0][0] if cast_counts else None
    predominant_director = director_counts.most_common(1)[0][0] if director_counts else None
    predominant_language = language_counts.most_common(1)[0][0] if language_counts else None

    return predominant_genre, predominant_cast, predominant_director, predominant_language

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
            str(x['genres_clean']),  
            ' '.join(cast_list[movie_history.index.get_loc(x.name)]),  
            ' '.join(directors_list[movie_history.index.get_loc(x.name)]),  
            ' '.join(languages_list[movie_history.index.get_loc(x.name)])  
        ]),
        axis=1
    )

    movie_history['filtered_soup'] = movie_history['soup'].apply(
        lambda x: ' '.join([token for token in x.split() if token in valid_tokens])
    )
    
    predominant_features = movie_history['filtered_soup'].apply(extract_predominant_from_soup)

    predominant_genres, predominant_cast, predominant_directors, predominant_languages = zip(*predominant_features)

    filters = {
        "genres": predominant_genres,
        "cast": predominant_cast,
        "directors": predominant_directors,
        "languages": predominant_languages
    }

    best_movie = query_filter_endpoint(filters)
    
    if best_movie:
        return {
            "source_movies": movie_history['title'].tolist(), 
            "recommended_movie": {
                "title": best_movie.get("title"),
                "id": best_movie.get("id"),
                "plot": best_movie.get("plot"),
                "genres": best_movie.get("genres"),
                "rating": best_movie.get("rating"),
                "poster": best_movie.get("poster")  
            }
        }

    random_movie = query_random_movie_endpoint(limit=1)
    
    return {
        "source_movies": movie_history['title'].tolist(),
        "recommended_movie": {
            "title": random_movie.get("title"),
            "id": random_movie.get("id"),
            "plot": random_movie.get("plot"),
            "genres": random_movie.get("genres"),
            "rating": random_movie.get("rating"),
            "poster": random_movie.get("poster")  
        }
    }