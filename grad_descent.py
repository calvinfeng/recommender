import csv_loader as loader
import numpy
from random import random
movie_set = './gd-10-movies/movies.csv'
rating_set = './gd-10-movies/ratings.csv'

#train_set_movies = loader.load_movies(movie_set, rating_set)
#train_set_users = loader.load_users(rating_set)

class Movie:
    def __init__(self, movie_id, viewers):
        self.id = movie_id
        self.viewers = viewers
        self.feature = self.random_init(8)

    def random_init(self, size):
        feature_vector = []
        while len(feature_vector) < size:
            feature_vector.append(random()**2)
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
            feature_vector.append(random()**2)
        return feature_vector

def gradient_descent(movies, users, a, lambda):
    for movie in movies:
        # this is movie i
        for k in range(0, len(movie.feature)):
            




my_movie = Movie(1, [1.5, 2.0, 3.0])
print my_movie.feature

my_user = User(1, [1.5, 1.5, 1.0])
print my_user.theta

print my_movie.hypothesis(my_user)
