import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

warnings.filterwarnings('ignore')

def clean_genres(genres):
    return ', '.join(str.lower(i.replace(" ", "")) for i in genres.split(', '))

def process_recommendations(movie_history_data, n=3):
  
    #Generate recommendations based on the movie history using cosine similarity within the history itself.

    #:param movie_history_data: List of movies from the history queue.
    #:param n: Number of recommendations for each movie in history.
    #:return: List of recommendations.

    movie_history = pd.DataFrame(movie_history_data)
    movie_history['genres_clean'] = movie_history['genres'].apply(clean_genres)
    movie_history['soup'] = movie_history.apply(
        lambda x: ' '.join([str(x['title']), str(x['genres_clean']), str(x['plot'])]),
        axis=1
    )

    count = CountVectorizer(analyzer='word', ngram_range=(1, 2), stop_words='english')
    count_matrix = count.fit_transform(movie_history['soup'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    recommendations = []

    for i, sim_scores in enumerate(cosine_sim):
        sorted_sim_scores = sorted(enumerate(sim_scores), key=lambda x: x[1], reverse=True)
        sorted_sim_scores = sorted_sim_scores[1:] 

        top_movies = sorted_sim_scores[:n]

        for movie in top_movies:
            movie_idx = movie[0]
            movie_details = movie_history.iloc[movie_idx]
            recommendations.append({
                "source_movie": movie_history.iloc[i]['title'], 
                "recommended_movie": {
                    "id": movie_details['id'],
                    "title": movie_details['title'],
                    "genres": movie_details['genres'],
                    "plot": movie_details['plot'],
                    "poster": movie_details['poster'],
                    "similarity_score": movie[1]  
                }
            })

    return recommendations