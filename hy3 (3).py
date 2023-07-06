import pandas as pd
import json
def read_ratings_data(filename):
    """
    Reads a movie ratings file and returns a dictionary with movie as key and a list of its ratings as value.
    
    Args:
    - filename: str, the name of the ratings file.
    
    Returns:
    - ratings_dict: dict, a dictionary with movie as key and a list of its ratings as value.
    """
    ratings_dict = {}
    with open(filename, 'r') as f:
        for line in f:
            movie, rating = line.strip().split('|')[:2]
            rating = float(rating)
            if movie not in ratings_dict:
                ratings_dict[movie] = [rating]
            else:
                ratings_dict[movie].append(rating)
    return ratings_dict

def read_movie_genre(f):
    movie_genre = {}
    with open(f, encoding='utf8') as file:
        for line in file:
            genre, movie_id, movie = line.strip().split("|")
            movie = movie.strip()
            genre = genre.strip()
            movie_genre[movie] = genre
    return movie_genre

def create_genre_dict(movie_to_genre):
    genre_to_movies = {}
    for movie, genre in movie_to_genre.items():
        movie = movie.strip()
        genre = genre.strip()
        if genre not in genre_to_movies:
            genre_to_movies[genre] = [movie]
        else:
            genre_to_movies[genre].append(movie)
    return genre_to_movies
def calculate_average_rating(ratings_dict):
    avg_ratings = {}
    for movie, ratings in ratings_dict.items():
        avg_ratings[movie] = sum(ratings) / len(ratings)
    return {movie: format(rating, '.2f') for movie, rating in avg_ratings.items()}

def get_popular_movies(avg_ratings_dict, n=10):
        # Sort the dictionary by value (average rating) in descending order
    sorted_movies = sorted(avg_ratings_dict.items(), key=lambda x: x[1], reverse=True)
    # Create a new dictionary of the top n movies
    popular_movies = dict(sorted_movies[:n])
    return popular_movies
def filter_movies(average_ratings, threshold=3):
    filtered_movies = {}
    for movie, rating in average_ratings.items():
        if float(rating) >= threshold:
            filtered_movies[movie] = rating
    return filtered_movies
def get_popular_in_genre(genre, genre_dict, avg_ratings_dict, n=5):
    genre_movies = genre_dict.get(genre, [])
    genre_ratings = {movie: avg_ratings_dict[movie] for movie in genre_movies if movie in avg_ratings_dict}
    sorted_movies = sorted(genre_ratings.items(), key=lambda x: x[1], reverse=True)
    result = dict(sorted_movies[:n])
    return result
def get_genre_rating(genre, genre_to_movies, movie_to_avg_rating):
    if genre not in genre_to_movies:
        return None
    
    movies_in_genre = genre_to_movies[genre]
    genre_rating_sum = 0.0
    genre_rating_count = 0
    
    for movie in movies_in_genre:
        if movie in movie_to_avg_rating:
            genre_rating_sum += float(movie_to_avg_rating[movie])
            genre_rating_count += 1
    
    if genre_rating_count == 0:
        return None
    
    return "{:.2f}".format(genre_rating_sum / genre_rating_count)


def genre_popularity(genre_to_movies, movie_to_avg_rating, n=5):
    genre_ratings = {}
    for genre in genre_to_movies:
        genre_rating = get_genre_rating(genre, genre_to_movies, movie_to_avg_rating)
        if genre_rating is not None:
            genre_ratings[genre] = genre_rating
    sorted_genres = sorted(genre_ratings.items(), key=lambda x: x[1], reverse=True)
    top_n_genres = sorted_genres[:n]
    return dict(top_n_genres)
def read_user_ratings(ratings_file):
    user_to_movies = {}
    with open(ratings_file) as file:
        for line in file:
            movie, rating, user = line.strip().split("|")
            if user not in user_to_movies:
                user_to_movies[user] = [(movie, rating)]
            else:
                user_to_movies[user].append((movie, rating))
    return user_to_movies
#user_ratings= read_user_ratings('ratings.txt')

def get_user_genre(user_id, user_to_movies, movie_to_genre):
    usr=read_user_ratings("ratings.txt")
    genre_to_ratings = {}
    for movie, rating in user_to_movies[user_id]:
        genre = movie_to_genre[movie]
        if genre not in genre_to_ratings:
            genre_to_ratings[genre] = []
        genre_to_ratings[genre].append(float(rating))
    
    genre_to_avg_rating = {genre: sum(ratings) / len(ratings) for genre, ratings in genre_to_ratings.items()}
    top_genre = max(genre_to_avg_rating, key=genre_to_avg_rating.get)
    return top_genre
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_avg_rating):
    user_ratings = user_to_movies
    ALREADYRATED = []
    for movie, rating in user_ratings[user_id]:
        ALREADYRATED.append(movie)    
    top_genre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    movies_to_recommend = [movie for movie, genre in movie_to_genre.items() if genre == top_genre and movie not in ALREADYRATED]

    if not movies_to_recommend:
        return f"User has already rated all movies in {top_genre} genre."

    movies_to_recommend = sorted(movies_to_recommend, key=lambda movie: movie_to_avg_rating.get(movie, 0), reverse=True)
    recommended_movies = {}
    for movie in movies_to_recommend:
        if len(recommended_movies) >= 3:
            break
        recommended_movies[movie] = movie_to_avg_rating[movie]

    return recommended_movies
#def main():
    # Define file paths
    #ratings_file = "ratings.txt"
    #movie_genre_file = "genre.txt"
    
    #1.1 
    #print(read_ratings_data(ratings_file))
    #1.2
    #print(read_movie_genre(movie_genre_file))
    #2.1
    #print(create_genre_dict(read_movie_genre(movie_genre_file)))
    #2.2
    #print(calculate_average_rating(read_ratings_data(ratings_file)))
    #3.1
    #print(get_popular_movies(calculate_average_rating(read_ratings_data(ratings_file))))
    #3.2
    #df =filter_movies(calculate_average_rating(read_ratings_data(ratings_file)))
    # print(df)
    #3.3
    #print(get_popular_in_genre("Adventure", create_genre_dict(read_movie_genre(movie_genre_file)), calculate_average_rating(read_ratings_data(ratings_file))))
    #3.4
    #print(get_genre_rating("Action", create_genre_dict(read_movie_genre(movie_genre_file)), calculate_average_rating(read_ratings_data(ratings_file))))
    #3.5
    #print(genre_popularity(create_genre_dict(read_movie_genre(movie_genre_file)), calculate_average_rating(read_ratings_data(ratings_file))))
    #4.1
    #print(read_user_ratings(ratings_file))
    #df = read_user_ratings(ratings_file)
    #pretty_ratings = json.dumps(df, indent=4)
    #print(pretty_ratings)
    #4.2
    #print(get_user_genre("1", read_user_ratings(ratings_file), read_movie_genre(movie_genre_file)))  
    #4.3
    #print(recommend_movies("1", read_user_ratings(ratings_file), read_movie_genre(movie_genre_file), calculate_average_rating(read_ratings_data(ratings_file))))
#if __name__ == "__main__":
  #  main() 