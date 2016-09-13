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
    load_user_ratings(movies)
    return movies

def load_user_ratings(movies):
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    number_of_ratings = 0
    for row in csv_reader:
        if row[0].isdigit():
            user_id = row[0]
            movie_id = row[1]
            rating = row[2]
            # Taking rating from only 10,000 users
            if int(user_id) <= 10000:
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

def load_users():
    users = dict()
    ratings_csv = open(SMALL_RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    for row in csv_reader:
        if row[0].isdigit():
            user_id, movie_id, rating = row[0], row[1], row[2]
            if users.get(user_id):
                users[user_id][movie_id] = rating
            else:
                users[user_id] = {movie_id: rating}
    return users

def reduce_set(movies):
    reduced_set = dict()
    for movie_id in movies:
        if movies[movie_id].get("ratings") and len(movies[movie_id]["ratings"]) >= 50:
            #print movies[movie_id]["title"]
            reduced_set[movie_id] = True
    print "Length: %s" % len(reduced_set)
    return reduced_set

def reduce_ratings_file(movie_set):
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    resized_ratings_csv = open('./ml-data/ratings.csv', 'wt')
    csv_writer = csv.writer(resized_ratings_csv)
    csv_writer.writerow(('userId', 'movieId', 'rating', 'timestamp'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and int(row[0]) <= 10000 and movie_set.get(row[1]):
            csv_writer.writerow((row[0], row[1], row[2], row[3]))
            write_count += 1
    print "Wrote %s items to ratings.csv" % write_count

def reduce_movie_file(movie_set):
    movies_csv = open(MOVIE_SET)
    csv_reader = csv.reader(movies_csv)
    resized_movies_csv = open('./ml-data/movies.csv', 'wt')
    csv_writer = csv.writer(resized_movies_csv)
    csv_writer.writerow(('movieId', 'title', 'genres'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and movie_set.get(row[0]):
            csv_writer.writerow((row[0], row[1], row[2]))
            write_count += 1
    print "Wrote %s items to movies.csv" % write_count

movies = load_movies()
movies_with_50_reviews = reduce_set(movies) # Movies with at least 50 reviews coming from 20,000 users
reduce_ratings_file(movies_with_50_reviews)
reduce_movie_file(movies_with_50_reviews)
