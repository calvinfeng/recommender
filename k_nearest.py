import pdb
import csv_loader as loader
from math import sqrt
from tabulate import tabulate

class User:
    def __init__(self, user_id, movie_ratings):
        self.id = user_id
        self.avg_rating = User.compute_avg_rating(movie_ratings)
        self.ratings = movie_ratings

    @staticmethod
    def compute_avg_rating(movie_ratings):
        avg_rating = 0
        for movie_id in movie_ratings:
            avg_rating += float(movie_ratings[movie_id])
        avg_rating = avg_rating/len(movie_ratings)
        return avg_rating

    def sim(user_1, user_2):
        # Using Pearson correlation coefficient
        user_correlation = 0
        user_1_variance, user_2_variance = 0, 0
        movies_seen_by_both = []
        for movie_id in user_1.ratings:
            if user_2.ratings.get(movie_id):
                movies_seen_by_both.append(movie_id)

        if len(movies_seen_by_both) >= 10:
            for movie_id in movies_seen_by_both:
                rating_1, rating_2 = float(user_1.ratings[movie_id]), float(user_2.ratings[movie_id])
                user_correlation += (rating_1 - user_1.avg_rating)*(rating_2 - user_2.avg_rating)
                user_1_variance += (rating_1 - user_1.avg_rating)**2
                user_2_variance += (rating_2 - user_2.avg_rating)**2
            if user_1_variance == 0 or user_2_variance == 0:
                # If one of the variances is zero, it's an undefined correlation
                return 0
            else:
                return user_correlation/(sqrt(user_1_variance)*sqrt(user_2_variance))
        else:
            # Statistically insignificant thus I return 0 for similarity
            return 0

class Movie:
    def __init__(self, movie_id, movie_title, user_ratings):
        self.id = movie_id
        self.title = movie_title
        self.avg_rating = Movie.compute_avg_ratings(user_ratings)
        self.num_of_ratings = len(user_ratings)
        self.ratings = user_ratings

    @staticmethod
    def compute_avg_ratings(user_ratings):
        avg_rating = 0
        for rating in user_ratings:
            avg_rating += float(rating)
        avg_rating = avg_rating/len(user_ratings)
        return avg_rating

def quick_sort(movies):
    if len(movies) <= 1:
        return movies
    else:
        pivot = movies[0]
        left, right = [], []
        for i in range(1, len(movies)):
            if movies[i].avg_rating > pivot.avg_rating:
                left.append(movies[i])
            else:
                right.append(movies[i])
        return quick_sort(left) + [pivot] + quick_sort(right)

# def qs(arr):
#     if len(arr) <= 1:
#         return arr
#     else:
#         pivot = arr[0]
#         left, right = [], []
#         for i in range(1, len(arr)):
#             if arr[i] <= pivot:
#                 left.append(arr[i])
#             else:
#                 right.append(arr[i])
#         return qs(left) + [pivot] + qs(right)
#
# print qs([9,8,7,6,5,4,3,2,1])
# users_data = loader.load_users()
# users = []
# for user_id in users_data:
#     users.append(User(user_id, users_data[user_id]))
# print "Number of users in database: %s \n" % len(users)
# for i in range(1, len(users)):
#     if User.sim(users[0], users[i]) > 0.75:
#         print "User 1 and User %s are similar: %s" % (i + 1, User.sim(users[0], users[i]))
#         movies_seen_by_both = []
#         user_1_ratings, user_2_ratings = [], []
#         for movie_id in users[0].ratings:
#             if users[i].ratings.get(movie_id):
#                 movies_seen_by_both.append(movie_id)
#                 user_1_ratings.append(users[0].ratings[movie_id])
#                 user_2_ratings.append(users[i].ratings[movie_id])
#         print tabulate([user_1_ratings, user_2_ratings],headers = movies_seen_by_both)
#         print "\n"

movies_data = loader.load_movies()
movies = []
for movie_id in movies_data:
    if movies_data[movie_id].get("viewers") and len(movies_data[movie_id]['viewers']) > 50:
        movies.append(Movie(movie_id, movies_data[movie_id]['title'], movies_data[movie_id]['ratings']))

movies = quick_sort(movies)
for movie in movies:
    print "%s has %s stars" % (movie.title, movie.avg_rating)
