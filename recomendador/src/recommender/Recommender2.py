from ..movies.UtilsMovies import get_movies_by_filter
from collections import Counter
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')
load_dotenv()

URL_MOVIES = os.getenv('URL_MOVIES')
LIMIT_MOVIES_SEARCH = os.getenv('LIMIT_MOVIES_SEARCH')

# Lista de peliculas que no se deben recomendar, ya que ya fueron recomendadas
black_list = []

def process_recommendations(movie_history_data):    
    movies_dataframe = prepare_recommendations(movie_history_data)
    recommended = recommend_movies(movie_history_data, movies_dataframe)
    best_movie = get_best_movie(recommended)
    black_list.append(best_movie["title"])    
    return best_movie

# Prepara el dataframe con las peliculas recomendadas para su posterior analisis
def prepare_recommendations(movie_history_data):
    filter = build_common_filter(movie_history_data)
    movies = get_movies_by_filter(filter, limit=LIMIT_MOVIES_SEARCH)
    movies = [movie for movie in movies if movie["title"] not in black_list]
    movies_dataframe = create_dataframe(movies)
    return movies_dataframe
        
def build_common_filter(movie_data):
    all_genres = []
    all_cast = []
    all_directors = []
    
    for movie in movie_data:        
        if "genres" in movie and movie["genres"]:
            all_genres.extend(movie["genres"])
        if "cast" in movie and movie["cast"]:
            all_cast.extend(movie["cast"])
        if "directors" in movie and movie["directors"]:
            all_directors.extend(movie["directors"])
    
    most_common_genre = Counter(all_genres).most_common(1)
    most_common_cast = Counter(all_cast).most_common(1)
    most_common_director = Counter(all_directors).most_common(1)
    
    return {
        "genres": [most_common_genre[0][0] if most_common_genre else None],
        "cast": [most_common_cast[0][0] if most_common_cast else None],
        "directors": [most_common_director[0][0] if most_common_director else None]
    }
    
def create_dataframe(movies_data):
    movies_pd = pd.DataFrame(movies_data)    

    movies_pd['genres_clean'] = movies_pd['genres'].apply(lambda x: ', '.join(genre.lower().replace(" ", "") for genre in x))
    #movies_pd['cast_clean'] = movies_pd['cast'].apply(lambda x: ', '.join(actor.lower().replace(" ", "") for actor in x))
    movies_pd['cast_clean'] = movies_pd['cast'].apply(
        lambda x: ', '.join(actor.lower().replace(" ", "") for actor in x) if isinstance(x, list) else ''
    )
    movies_pd['directors_clean'] = movies_pd['directors'].apply(
        lambda x: ', '.join(director.lower().replace(" ", "") for director in x) if isinstance(x, list) else ''
    )
    
    movies_pd['soup'] = movies_pd.apply(lambda x: ' '.join([str(x['title']), str(x['genres_clean']), str(x['cast_clean']), str(x['directors_clean'])]), axis=1)    
    return movies_pd

# Por cada pelicula en la lista, recomienda una pelicula
# Luego devuelve la mejor pelicula segun el rating ponderado y la cantidad de votos
def recommend_movies(movies, movies_pd):
    recommended_movies = []
    for movie in movies:
        recommended_movie = recommend_movie(movies_pd, movie["title"])
        recommended_movies.append(recommended_movie.iloc[0].to_dict())
    return recommended_movies

def recommend_movie(movies_pd, title, n=10, self_exclude=True):    
    cosine_sim = calculate_cosine_similarity_matrix(movies_pd)
    idx = get_movie_index(movies_pd, title, cosine_sim)
    sim_scores = get_similar_movies(cosine_sim, idx, n, self_exclude)
    
    movie_indices = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores]
    
    recommended_movies = movies_pd.iloc[movie_indices].copy()
    recommended_movies['sim_score'] = scores
    
    return recommended_movies

def calculate_cosine_similarity_matrix(movies_pd):    
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0, stop_words='english')
    count_matrix = vectorizer.fit_transform(movies_pd['soup'])
    return cosine_similarity(count_matrix, count_matrix)

def get_movie_index(movies_pd, title, cosine_sim):    
    indices = pd.Series(movies_pd.index, index=movies_pd['title'])
    try:        
        idx = indices[title]
    except KeyError:        
        idx = max(enumerate(cosine_sim), key=lambda x: max(x[1]))[0]
    return idx

def get_similar_movies(cosine_sim, idx, n=10, self_exclude=True):    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    if self_exclude:
        sim_scores = sim_scores[1:n+1]
    else:
        sim_scores = sim_scores[0:n+1]

    return sim_scores

# En base a una lista de peliculas, devuelve la mejor pelicula segun el rating ponderado y la cantidad de votos
def get_best_movie(movies):    
    movies_with_wr = calculate_weighted_rating(movies)
    best_movie = max(movies_with_wr, key=lambda x: x['weighted_rating'])
    return best_movie

def calculate_weighted_rating(movies):
    votes = np.array([movie["imdb"]["votes"] for movie in movies])    
    c = np.median(votes)
    
    for movie in movies:
        rating = movie['imdb']['rating']
        votes_count = movie['imdb']['votes']
            
        movie['weighted_rating'] = (votes_count * rating) / (votes_count + c)
    
    return movies
