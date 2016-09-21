import csv_loader as loader
import numpy
import pdb
from random import random

movie_set = './gd-10-movies/movies.csv'
rating_set = './gd-10-movies/ratings.csv'

class Movie:
    def __init__(self, movie_id, title, viewers):
        self.id = movie_id
        self.title = title
        self.viewers = viewers
        self.feature = self.random_init(8)

    def random_init(self, size):
        feature_vector = []
        while len(feature_vector) < size:
            feature_vector.append(random())
        return feature_vector

    def hypothesis(self, user):
        return numpy.dot(self.feature, user.theta)

class User:
    def __init__(self, user_id, movie_ratings):
        self.id = user_id
        self.movie_ratings = movie_ratings
        self.theta = self.random_init(8)

    def random_init(self, size):
        feature_vector = []
        while len(feature_vector) < size:
            feature_vector.append(random())
        return feature_vector

def cost_function(movies, users, l):
    sq_error = 0
    for movie_id in movies:
        movie = movies[movie_id]
        viewers = movie.viewers
        for user_id in viewers:
            user = users[user_id]
            sq_error += (movie.hypothesis(user) - float(user.movie_ratings[movie.id]))**2
    sq_error *= 0.5

    regularized_term = 0
    for movie_id in movies:
        movie = movies[movie_id]
        for k in range(0, len(movie.feature)):
            regularized_term += movie.feature[k]**2

    for user_id in users:
        user = users[user_id]
        for k in range(0, len(user.theta)):
            regularized_term += user.theta[k]**2

    return regularized_term*(l/2) + sq_error

# wrt = with respect to
def dj_wrt_movie_feature_k(movie, users, l, k):
    derivative_sum = 0
    for user_id in movie.viewers:
        user = users[user_id]
        temp = movie.hypothesis(user) - float(user.movie_ratings[movie.id])
        temp *= user.theta[k]
        derivative_sum += temp
    return derivative_sum + l*movie.feature[k]

# wrt = with respect to
def dj_wrt_user_theta_k(user, movies, l, k):
    derivative_sum = 0
    for movie_id in user.movie_ratings:
        movie = movies[movie_id]
        temp = (movie.hypothesis(user) - float(user.movie_ratings[movie_id]))
        temp *= movie.feature[k]
        derivative_sum += temp
    return derivative_sum + l*user.theta[k]

# def gradient_descent(movies, users, a, l):
#     while True:
#         print "Cost: %s" % (cost_function(movies, users, l))
#     return None

train_set_movies = loader.load_movies(movie_set, rating_set)
train_set_users = loader.load_users(rating_set)

movies = dict()
for movie_id in train_set_movies:
    movies[movie_id] = Movie(movie_id,train_set_movies[movie_id]["title"], train_set_movies[movie_id]["viewers"])
users = dict()
for user_id in train_set_users:
    users[user_id] = User(user_id, train_set_users[user_id])

print cost_function(movies, users, 0.01)
for movie_id in movies:
    movie = movies[movie_id]
    print movie.title
    for k in range(0, len(movie.feature)):
        print "Derivative w.r.t movie feature k: %s" % (dj_wrt_movie_feature_k(movie, users, 0.01, k))

for user_id in users:
    user = users[user_id]
    print "User #%s" % user.id
    for k in range(0, len(user.theta)):
        print "Derivative w.r.t user theta k: %s" % (dj_wrt_user_theta_k(user, movies, 0.01, k))
