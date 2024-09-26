import random

# Simulated weather data for random cities
weather_data = {
    "New York": ["clear sky", "rain", "snow", "cloudy"],
    "London": ["rain", "cloudy", "clear sky", "fog"],
    "Tokyo": ["clear sky", "rain", "cloudy"],
    "Mumbai": ["sunny", "rain", "cloudy", "humid"],
    "Sydney": ["clear sky", "windy", "rain"],
}

# Simulated movie data for random genres
movies_data = {
    "Adventure": [
        {"title": "Indiana Jones", "year": 1981},
        {"title": "Jurassic Park", "year": 1993},
        {"title": "The Lord of the Rings", "year": 2001},
    ],
    "Drama": [
        {"title": "The Godfather", "year": 1972},
        {"title": "Forrest Gump", "year": 1994},
        {"title": "The Shawshank Redemption", "year": 1994},
    ],
    "Comedy": [
        {"title": "Superbad", "year": 2007},
        {"title": "The Hangover", "year": 2009},
        {"title": "Groundhog Day", "year": 1993},
    ],
    "Action": [
        {"title": "Die Hard", "year": 1988},
        {"title": "Mad Max: Fury Road", "year": 2015},
        {"title": "John Wick", "year": 2014},
    ],
}


def get_random_weather(city):
    """Simulates getting random weather data for a given city."""
    if city in weather_data:
        return random.choice(weather_data[city])
    else:
        return random.choice(["clear sky", "rain", "cloudy", "windy"])


def get_random_movies(genre):
    """Simulates getting random movie data for a given genre."""
    if genre in movies_data:
        return random.sample(movies_data[genre], 2)  # return 2 random movies
    else:
        return random.sample(movies_data["Action"], 2)  # fallback to Action genre


from flask import Flask, jsonify, request
from flask_limiter import Limiter

app = Flask(__name__)

# Define your API key (for real-world applications, store this securely)
API_KEY = "mysecretapikey"

# Set up Flask-Limiter with key function defined
limiter = Limiter(
    key_func=lambda: request.headers.get("x-api-key"),  # Use API key as the key for rate limiting
    default_limits=["1 per 2 seconds"],  # Set default rate limit
)

# Attach limiter to the app
limiter.init_app(app)


# Utility function to verify the API key from headers
def check_api_key(request):
    api_key = request.headers.get("x-api-key")  # Get API key from headers
    return api_key == API_KEY


# Weather API Route with API key authentication and rate limiting
@app.route("/api/weather", methods=["GET"])
def get_weather():
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized: Invalid API Key"}), 401

    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City not provided"}), 400

    weather = get_random_weather(city)

    return jsonify({"city": city, "weather": weather})


# Movies API Route with API key authentication and rate limiting
@app.route("/api/movies", methods=["GET"])
def get_movies():
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized: Invalid API Key"}), 401

    genre = request.args.get("genre")
    if not genre:
        return jsonify({"error": "Genre not provided"}), 400

    movies = get_random_movies(genre)

    return jsonify({"genre": genre, "movies": movies})


# Error handling for invalid routes
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


# Error handling for rate limiting
@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({"error": "ratelimit exceeded", "message": str(e.description)}), 429


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
