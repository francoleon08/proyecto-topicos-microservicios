from flask import Flask, jsonify
import threading
from .rabbit.RabbitConection import init_connection, consume_movies
from .recommender.Recommender import process_recommendations

app = Flask(__name__)

#movies = []

movies = [
    {
        "_id": "573a139bf29313caabcf5017",
        "countries": [
            "France",
            "Iceland",
            "Sweden"
        ],
        "genres": [
            "Drama",
            "History"
        ],
        "runtime": 122,
        "cast": [
            "Tinna Gunnlaugsdèttir",
            "Pierre Vaneck",
            "Sigursteinn Brynjèlfsson",
            "Christian Charmetant"
        ],
        "num_mflix_comments": 1,
        "title": "As in Heaven",
        "lastupdated": "2015-08-29 23:54:01.257000000",
        "languages": [
            "Icelandic",
            "French"
        ],
        "released": "1992-08-29T00:00:00.000Z",
        "directors": [
            "Kristèn Jèhannesdèttir"
        ],
        "writers": [
            "Kristèn Jèhannesdèttir"
        ],
        "awards": {
            "wins": 2,
            "nominations": 1,
            "text": "2 wins & 1 nomination."
        },
        "year": 1992,
        "imdb": {
            "rating": 7.1,
            "votes": 41,
            "id": 105504
        },
        "type": "movie"
    },
    {
        "_id": "573a13a8f29313caabd1c771",
        "plot": "An exuberant, sharply satirical comedy about two parentally neglected teenagers who find the courage to believe in themselves",
        "genres": [
            "Comedy"
        ],
        "runtime": 89,
        "metacritic": 63,
        "cast": [
            "Jordan Brooking",
            "Ben Lee",
            "Rose Byrne",
            "Miranda Richardson"
        ],
        "num_mflix_comments": 1,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTI4Njg1MTA2M15BMl5BanBnXkFtZTcwODIwODc0MQ@@._V1_SY1000_SX677_AL_.jpg",
        "title": "The Rage in Placid Lake",
        "fullplot": "Precocious, bohemian teenager Placid Lake, finishes high school and decides to do the one thing that will annoy his new age parents the most--go straight! With a few weeks spent reading a library of self-help manuals, Placid has it all sorted out--and he has the haircut and the cheap suit to prove it. Can Placid Lake retire his rage in the pursuit of beige; embrace conformity and leap on the fast track to corporate success. Will his 'brainiac' friend Gemma be able to talk him out of this economic rationalist madness? And will poor Doug and Sylvia survive the ignominy of having a son with a burgeoning future in insurance? Never underestimate the evil of banality.",
        "languages": [
            "English"
        ],
        "released": "2003-08-28T00:00:00.000Z",
        "directors": [
            "Tony McNamara"
        ],
        "writers": [
            "Tony McNamara"
        ],
        "awards": {
            "wins": 4,
            "nominations": 12,
            "text": "4 wins & 12 nominations."
        },
        "lastupdated": "2015-08-30 00:27:10.040000000",
        "year": 2003,
        "imdb": {
            "rating": 7.1,
            "votes": 2479,
            "id": 305999
        },
        "countries": [
            "Australia"
        ],
        "type": "movie",
        "tomatoes": {
            "website": "http://www.filmmovement.com/FilmDetail.aspx?ProductID=0504",
            "viewer": {
                "rating": 3.7,
                "numReviews": 5479,
                "meter": 79
            },
            "dvd": "2006-04-18T00:00:00.000Z",
            "critic": {
                "rating": 6.1,
                "numReviews": 15,
                "meter": 53
            },
            "lastUpdated": "2015-09-14T19:59:52.000Z",
            "rotten": 7,
            "production": "Film Movement",
            "fresh": 8
        }
    },
    {
        "_id": "573a13ccf29313caabd831f3",
        "plot": "A drama about a woman who seems able to overcome everything for freedom, except for her past mistakes.",
        "genres": [
            "Action",
            "Drama"
        ],
        "runtime": 87,
        "cast": [
            "Ana Ularu",
            "Andi Vasluianu",
            "Ioana Flora",
            "Mimi Branescu"
        ],
        "poster": "https://m.media-amazon.com/images/M/MV5BM2RlOWQ4Y2YtYjVkOS00OTk3LTkzYzktYTcyNzllYjhlYWE2XkEyXkFqcGdeQXVyNDkzNTM2ODg@._V1_SY1000_SX677_AL_.jpg",
        "title": "Outbound",
        "fullplot": "After two years in prison, Matilda is granted a 24-hour temporary release. Not willing to return, she plans to escape, flee the country and start afresh. But before the day is over, Matilda must reconnect with her troubled past - the family who rejected her, her estranged ex-lover and, most of all, the kid she left behind. The struggle for a new life reminds her that freedom may be just one choice away.",
        "languages": [
            "Romanian"
        ],
        "released": "2011-03-24T00:00:00.000Z",
        "directors": [
            "Bogdan George Apetri"
        ],
        "writers": [
            "Bogdan George Apetri (screenplay)",
            "Cristian Mungiu (story)",
            "Ioana Uricaru (story)",
            "Tudor Voican (screenplay)"
        ],
        "awards": {
            "wins": 20,
            "nominations": 10,
            "text": "20 wins & 10 nominations."
        },
        "lastupdated": "2015-08-15 00:47:43.753000000",
        "year": 2010,
        "imdb": {
            "rating": 6.7,
            "votes": 616,
            "id": 1646221
        },
        "countries": [
            "Romania",
            "Austria"
        ],
        "type": "movie",
        "num_mflix_comments": 0
    },
    {
        "_id": "573a13d3f29313caabd943da",
        "plot": "The story is about the world of a small family with familiar dreams and not so remarkable problems. The mother is trying to lead everything to save her family, but small events disarrange all her plans.",
        "genres": [
            "Drama",
            "Family"
        ],
        "runtime": 100,
        "cast": [
            "Saber Abbar",
            "Negar Javaherian",
            "Fatemah Motamed-Aria",
            "Parsa Pirouzfar"
        ],
        "num_mflix_comments": 0,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTU3MTk5OTkzMV5BMl5BanBnXkFtZTcwMDI1NjIzNw@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Here Without Me",
        "fullplot": "The story is about the world of a small family with familiar dreams and not so remarkable problems. The mother is trying to lead everything to save her family, but small events disarrange all her plans.",
        "languages": [
            "Persian"
        ],
        "released": "2012-03-23T00:00:00.000Z",
        "directors": [
            "Bahram Tavakoli"
        ],
        "writers": [
            "Bahram Tavakoli",
            "Tennessee Williams (play)"
        ],
        "awards": {
            "wins": 1,
            "nominations": 1,
            "text": "1 win & 1 nomination."
        },
        "lastupdated": "2015-07-28 00:29:29.420000000",
        "year": 2011,
        "imdb": {
            "rating": 8.1,
            "votes": 2832,
            "id": 1874522
        },
        "countries": [
            "Iran"
        ],
        "type": "movie",
        "tomatoes": {
            "viewer": {
                "rating": 3.9,
                "numReviews": 22
            },
            "lastUpdated": "2015-06-25T20:25:26.000Z"
        }
    }
]

def start_consumer():
    channel = init_connection()
    consume_movies(channel)

@app.route('/', methods=['GET'])
def get_recommendations():
    if len(movies) == 0:
        return jsonify({"message": "No recommendations yet"}), 404

    recommendations = process_recommendations(movies)
    #return jsonify({"recommendations": recommendations})
    return recommendations

if __name__ == '__main__':
    threading.Thread(target=start_consumer, daemon=True).start()

    app.run(host='0.0.0.0', port=5000, debug=True)