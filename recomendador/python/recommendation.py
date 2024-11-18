import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import sys
import warnings
warnings.filterwarnings('ignore')

movies_to_analyze = pd.read_csv('./database/movies.csv')
recommendable_movies = pd.read_csv('./database/recommendable_movies.csv')

def clean_genres(genres):
    return ', '.join(str.lower(i.replace(" ", "")) for i in genres.split(', '))

movies_to_analyze['genres_clean'] = movies_to_analyze['genres'].apply(clean_genres)
recommendable_movies['genres_clean'] = recommendable_movies['genres'].apply(clean_genres)

movies_to_analyze['soup'] = movies_to_analyze.apply(
    lambda x: ' '.join([str(x['title']), str(x['genres_clean'])]),
    axis=1
)
recommendable_movies['soup'] = recommendable_movies.apply(
    lambda x: ' '.join([str(x['title']), str(x['genres_clean'])]),
    axis=1
)

count = CountVectorizer(analyzer='word', ngram_range=(1, 2), stop_words='english')
count_matrix = count.fit_transform(recommendable_movies['soup'])

def recommend_movie_from_batch(title, n=1, self_exclude=True):
    recommendations = []

    try:
        idx = movies_to_analyze[movies_to_analyze['title'] == title].index[0]
    except IndexError:
        movie_soup = ' '.join([str(title), ''])
        movie_vec = count.transform([movie_soup])
        cosine_sim = cosine_similarity(movie_vec, count_matrix)
        idx = np.argmax(cosine_sim)

    movie_soup = movies_to_analyze.iloc[idx]['soup']
    movie_vec = count.transform([movie_soup])
    cosine_sim = cosine_similarity(movie_vec, count_matrix)

    sim_scores = list(enumerate(cosine_sim[0]))
    sorted_sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    if self_exclude:
        sorted_sim_scores = sorted_sim_scores[1:]

    top_movies = sorted_sim_scores[:n]

    for movie in top_movies:
        movie_idx = movie[0]
        movie_details = recommendable_movies.iloc[movie_idx]
        recommendations.append({
            "id": movie_details['id'],                
            "plot": movie_details['plot'],            
            "poster": movie_details['poster'],        
            "title": movie_details['title']          
        })

    return recommendations