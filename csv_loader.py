import csv
import pdb

def load_movies(movie_file_location, rating_file_location):
    movies = dict()
    movies_csv = open(movie_file_location)
    csv_reader = csv.reader(movies_csv)
    for row in csv_reader:
        if row[0].isdigit():
            movie_id = row[0]
            movie_title = row[1]
            movie_year = row[2]
            movies[movie_id] = {"title": movie_title, "year": movie_year}
    load_user_ratings(movies, rating_file_location)
    print "Loaded CSV...number of movies: %s" % len(movies)
    return movies

def load_user_ratings(movies, rating_file_location):
    ratings_csv = open(rating_file_location)
    csv_reader = csv.reader(ratings_csv)
    number_of_ratings = 0
    for row in csv_reader:
        if row[0].isdigit():
            user_id = row[0]
            movie_id = row[1]
            rating = row[2]
            number_of_ratings += 1
            if movies[movie_id].get("ratings"):
                movies[movie_id]["ratings"].append(rating)
                movies[movie_id]["viewers"].append(user_id)
            else:
                movies[movie_id]["ratings"] = [rating]
                movies[movie_id]["viewers"] = [user_id]
    print "Loaded CSV...number of ratings: %s" % (number_of_ratings)

def load_users(rating_file_location):
    users = dict()
    ratings_csv = open(rating_file_location)
    csv_reader = csv.reader(ratings_csv)
    for row in csv_reader:
        if row[0].isdigit():
            user_id, movie_id, rating = row[0], row[1], row[2]
            if users.get(user_id):
                users[user_id][movie_id] = rating
            else:
                users[user_id] = {movie_id: rating}
    print "Loaded CSV...number of users: %s" % len(users)
    return users

def compute_avg_ratings(movies):
    for movie_id in movies:
        if movies[movie_id].get("ratings"):
            total_rating = 0
            for rating in movies[movie_id]["ratings"]:
                total_rating += float(rating)
                movies[movie_id]["avg_rating"] = total_rating/len(movies[movie_id]["viewers"])
    return movies
