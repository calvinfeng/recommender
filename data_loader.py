import csv
import pdb

SMALL_MOVIE_SET = './ml-latest-small/movies.csv'
SMALL_RATING_SET = './ml-latest-small/ratings.csv'
MOVIE_SET = './ml-latest/movies.csv'
RATING_SET = './ml-latest/ratings.csv'

def load_movies():
    movies = dict()
    movies_csv = open(MOVIE_SET)
    csv_reader = csv.reader(movies_csv)
    for row in csv_reader:
        if row[0].isdigit():
            movie_id = row[0]
            movie_title = row[1]
            movies[movie_id] = {"title": movie_title}
    return movies

def load_user_ratings(movies):
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    for row in csv_reader:
        if row[0].isdigit():
            movie_id = row[1]
            rating = row[2]
            if movies[movie_id].get("rating"):
                movies[movie_id]["rating"].append(rating)
            else:
                movies[movie_id]["rating"] = [rating]
    return movies

movies = load_movies()
load_user_ratings(movies)
for key in movies:
    if not movies[key].get("rating"):
        print movies[key]["title"]
    #print movies[key]["rating"]
print "Movies count: %s" % len(movies)
