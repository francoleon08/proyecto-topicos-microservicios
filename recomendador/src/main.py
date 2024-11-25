from flask import Flask, jsonify
import threading
from .rabbit.RabbitConection import init_connection, consume_movies
from .recommender.Recommender import process_recommendations

app = Flask(__name__)

#movies = []

movies = [
    {
        "_id": "573a1398f29313caabcea92f",
        "plot": "The supposed true story of Shirley MacClaine's experience with a spiritual awakening.",
        "genres": [
            "Biography",
            "Drama"
        ],
        "runtime": 235,
        "cast": [
            "Shirley MacLaine",
            "Charles Dance",
            "John Heard",
            "Anne Jackson"
        ],
        "num_mflix_comments": 0,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTU2MTEzODQ2M15BMl5BanBnXkFtZTcwNTgzNzAyMQ@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Out on a Limb",
        "fullplot": "Shirley MacLaine plays herself in this TV mini-series based on her autobiographical best-seller which delves into her new age beliefs and its effects on her personal and public lives. John Heard portrays a composite role of her many spiritual and personal advisors.",
        "languages": [
            "English"
        ],
        "released": "1987-01-18T00:00:00.000Z",
        "awards": {
            "wins": 0,
            "nominations": 4,
            "text": "Nominated for 1 Golden Globe. Another 3 nominations."
        },
        "lastupdated": "2015-07-23 00:30:21.850000000",
        "year": 1987,
        "imdb": {
            "rating": 7.2,
            "votes": 353,
            "id": 93688
        },
        "countries": [
            "USA"
        ],
        "type": "series",
        "tomatoes": {
            "viewer": {
                "rating": 3.8,
                "numReviews": 20,
                "meter": 71
            },
            "dvd": "1992-11-04T00:00:00.000Z",
            "lastUpdated": "2015-06-24T19:12:31.000Z"
        }
    },
    {
        "_id": "573a1393f29313caabcdcf84",
        "plot": "Sara and Kurt Muller and their three children are returning to her mother's home in Washington DC after 18 years in Europe. A Romanian Count living there discovers Kurt's attache case full ...",
        "genres": [
            "Drama"
        ],
        "runtime": 114,
        "rated": "APPROVED",
        "cast": [
            "Bette Davis",
            "Paul Lukas",
            "Geraldine Fitzgerald",
            "Lucile Watson"
        ],
        "num_mflix_comments": 0,
        "poster": "https://m.media-amazon.com/images/M/MV5BM2ZmMDhjNmQtN2MxNy00MTdmLTg4MTEtZTVkMTFmZDg0NTNlXkEyXkFqcGdeQXVyMDI2NDg0NQ@@._V1_SY1000_SX677_AL_.jpg",
        "title": "Watch on the Rhine",
        "fullplot": "Sara and Kurt Muller and their three children are returning to her mother's home in Washington DC after 18 years in Europe. A Romanian Count living there discovers Kurt's attache case full of money. He also finds out from friends at the German Embassy that Kurt is working with an anti-Nazi underground group in Germany. He tries to blackmail Kurt. Kurt shoots him and must flee. When Sara hears no more of Kurt, she knows that her oldest son Joshua will soon leave to work in the underground.",
        "languages": [
            "English",
            "German"
        ],
        "released": "1943-08-27T00:00:00.000Z",
        "directors": [
            "Herman Shumlin",
            "Hal Mohr"
        ],
        "writers": [
            "Dashiell Hammett (screen play)",
            "Lillian Hellman (additional scenes and dialogue)",
            "Lillian Hellman (from the stage play by)"
        ],
        "awards": {
            "wins": 5,
            "nominations": 3,
            "text": "Won 1 Oscar. Another 4 wins & 3 nominations."
        },
        "lastupdated": "2015-08-18 00:26:01.173000000",
        "year": 1943,
        "imdb": {
            "rating": 7.5,
            "votes": 2510,
            "id": 36515
        },
        "countries": [
            "USA"
        ],
        "type": "movie",
        "tomatoes": {
            "viewer": {
                "rating": 3.6,
                "numReviews": 564,
                "meter": 63
            },
            "dvd": "2008-04-01T00:00:00.000Z",
            "critic": {
                "rating": 6.8,
                "numReviews": 5,
                "meter": 80
            },
            "lastUpdated": "2015-09-10T19:15:55.000Z",
            "rotten": 1,
            "production": "Warner Home Video",
            "fresh": 4
        }
    },
    {
        "_id": "573a13b1f29313caabd36bd7",
        "fullplot": "Anthony \"Swoff\" Swofford, a Camus-reading kid from Sacramento, enlists in the Marines in the late 1980s. He malingers during boot camp, but makes it through as a sniper, paired with the usually-reliable Troy. The Gulf War breaks out, and his unit goes to Saudi Arabia for Desert Shield. After 175 days of boredom, adrenaline, heat, worry about his girlfriend finding someone else, losing it and nearly killing a mate, demotion, latrine cleaning, faulty gas masks, and desert football, Desert Storm begins. In less than five days, it's over, but not before Swoff sees burned bodies, flaming oil derricks, an oil-drenched horse, and maybe a chance at killing. Where does all the testosterone go?",
        "imdb": {
            "rating": 7.1,
            "votes": 133309,
            "id": 418763
        },
        "year": 2005,
        "plot": "Based on former Marine Anthony Swofford's best-selling 2003 book about his pre-Desert Storm experiences in Saudi Arabia and about his experiences fighting in Kuwait.",
        "genres": [
            "Drama",
            "War"
        ],
        "rated": "R",
        "metacritic": 58,
        "title": "Jarhead",
        "lastupdated": "2015-08-25 00:09:40.870000000",
        "languages": [
            "English",
            "Spanish",
            "Arabic",
            "Latin"
        ],
        "writers": [
            "William Broyles Jr. (screenplay)",
            "Anthony Swofford (book)"
        ],
        "type": "movie",
        "tomatoes": {
            "website": "http://www.jarheadmovie.com/",
            "viewer": {
                "rating": 3.3,
                "numReviews": 391985,
                "meter": 68
            },
            "dvd": "2006-03-07T00:00:00.000Z",
            "critic": {
                "rating": 6.4,
                "numReviews": 196,
                "meter": 61
            },
            "boxOffice": "$62.6M",
            "consensus": "This first person account of the first Gulf War scores with its performances and cinematography but lacks an emotional thrust.",
            "rotten": 76,
            "production": "Universal Pictures",
            "lastUpdated": "2015-09-15T20:09:50.000Z",
            "fresh": 120
        },
        "poster": "https://m.media-amazon.com/images/M/MV5BYmMyNGM4NWItYjgwYS00N2Q2LWJmY2YtY2ViNWYwMzRhODlmXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SY1000_SX677_AL_.jpg",
        "num_mflix_comments": 0,
        "released": "2005-11-04T00:00:00.000Z",
        "awards": {
            "wins": 5,
            "nominations": 11,
            "text": "5 wins & 11 nominations."
        },
        "countries": [
            "Germany",
            "USA"
        ],
        "cast": [
            "Jake Gyllenhaal",
            "Scott MacDonald",
            "Peter Sarsgaard",
            "Jamie Foxx"
        ],
        "directors": [
            "Sam Mendes"
        ],
        "runtime": 125
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