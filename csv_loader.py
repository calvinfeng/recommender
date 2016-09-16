import csv
import pdb

SMALL_MOVIE_SET = './ml-latest-small/movies.csv'
SMALL_RATING_SET = './ml-latest-small/ratings.csv'

MOVIE_SET = './ml-latest/movies.csv'
RATING_SET = './ml-latest/ratings.csv'

MED_RATING_SET = './ml-data/ratings.csv'
def load_movies():
    movies = dict()
    movies_csv = open(MOVIE_SET)
    csv_reader = csv.reader(movies_csv)
    for row in csv_reader:
        if row[0].isdigit():
            movie_id = row[0]
            movie_title = row[1]
            movies[movie_id] = {"title": movie_title}
    # Taking rating from the first 10,000 users
    load_user_ratings(movies, 10000)
    return movies

def load_user_ratings(movies, num_of_users):
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    number_of_ratings = 0
    for row in csv_reader:
        if row[0].isdigit():
            user_id = row[0]
            movie_id = row[1]
            rating = row[2]
            if int(user_id) <= num_of_users:
                number_of_ratings += 1
                if movies[movie_id].get("ratings"):
                    movies[movie_id]["ratings"].append(rating)
                    movies[movie_id]["viewers"].append(user_id)
                else:
                    movies[movie_id]["ratings"] = [rating]
                    movies[movie_id]["viewers"] = [user_id]
    print "Number of ratings: %s" % (number_of_ratings)


def compute_avg_ratings(movies):
    for movie_id in movies:
        if movies[movie_id].get("ratings"):
            total_rating = 0
            for rating in movies[movie_id]["ratings"]:
                total_rating += float(rating)
                movies[movie_id]["avg_rating"] = total_rating/len(movies[movie_id]["viewers"])
    return movies

def load_users(start, end):
    users = dict()
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    for row in csv_reader:
        if row[0].isdigit():
            user_id, movie_id, rating = row[0], row[1], row[2]
            if start <= int(user_id) and int(user_id) <= end:
                if users.get(user_id):
                    users[user_id][movie_id] = rating
                else:
                    users[user_id] = {movie_id: rating}
    return users
