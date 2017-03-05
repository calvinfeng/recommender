# Project: Recommender System
# Author(s): Calvin Feng

from numpy import dot
from random import random

class Movie:
    def __init__(self, movie_id, title, viewers, ratings):
        self.id = movie_id
        self.title = title
        self.viewers = viewers
        self.ratings = ratings
        self.feature = self.random_init(8)

    def random_init(self, size):
        feature_vector = []
        while len(feature_vector) < size:
            feature_vector.append(random())
        return feature_vector

    def hypothesis(self, user):
        return dot(self.feature, user.theta)
