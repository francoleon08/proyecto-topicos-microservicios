from flask import Flask, jsonify
from rabbit.rabbitmq_manager import fetch_movie_history_from_queue, send_recommendations_to_queue
from recommender.recommender import process_recommendations

app = Flask(__name__)

@app.route('/process_movies', methods=['POST'])
def process_movies():
    try:
        
        movie_history = fetch_movie_history_from_queue()

        if not movie_history:
            return jsonify({"message": "No movie history found in queue"}), 400

        recommendations = process_recommendations(movie_history)

        send_recommendations_to_queue(recommendations)

        return jsonify({"message": "Recommendations processed successfully", "recommendations": recommendations}), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "Failed to process movies"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)