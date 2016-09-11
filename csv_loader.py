import csv
import pdb

SMALL_MOVIE_SET = './ml-latest-small/movies.csv'
SMALL_RATING_SET = './ml-latest-small/ratings.csv'
MOVIE_SET = './ml-latest/movies.csv'
RATING_SET = './ml-latest/ratings.csv'

def load_movies():
    movies = dict()
    movies_csv = open(SMALL_MOVIE_SET)
    csv_reader = csv.reader(movies_csv)
    for row in csv_reader:
        if row[0].isdigit():
            movie_id = row[0]
            movie_title = row[1]
            movies[movie_id] = {"title": movie_title}
    load_user_ratings(movies)
    return movies

def load_user_ratings(movies):
    ratings_csv = open(SMALL_RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    for row in csv_reader:
        if row[0].isdigit():
            user_id = row[0]
            movie_id = row[1]
            rating = row[2]
            if movies[movie_id].get("ratings"):
                movies[movie_id]["ratings"].append(rating)
                movies[movie_id]["viewers"].append(user_id)
            else:
                movies[movie_id]["ratings"] = [rating]
                movies[movie_id]["viewers"] = [user_id]
    return movies

def compute_avg_ratings(movies):
    for movie_id in movies:
        if movies[movie_id].get("ratings"):
            total_rating = 0
            for rating in movies[movie_id]["ratings"]:
                total_rating += float(rating)
                movies[movie_id]["avg_rating"] = total_rating/len(movies[movie_id]["viewers"])
    return movies

def load_users():
    users = dict()
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    for row in csv_reader:
        if row[0].isdigit():
            user_id, movie_id, rating = row[0], row[1], row[2]
            if users.get(user_id):
                users[user_id][movie_id] = rating
            else:
                users[user_id] = {movie_id: rating}
    return users
