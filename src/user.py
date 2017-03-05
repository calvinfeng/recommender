# Project: Recommender System
# Author(s): Calvin Feng

from random import random, sample

class User:
    def __init__(self, user_id, movie_ratings, is_test_user=False):
        self.id = user_id
        self.theta = self.random_init(8)
        if is_test_user:
            self.set_ratings(movie_ratings, 2)
        else:
            self.set_ratings(movie_ratings, 0)

    def random_init(self, size):
        # Give User a bias term, which is 1
        preference_vector = [1]
        while len(preference_vector) < size:
            preference_vector.append(random())
        return preference_vector

    def set_ratings(self, movie_ratings, num_of_hidden_ratings):
        hidden_ratings = dict()
        random_keys = sample(movie_ratings, num_of_hidden_ratings)
        for i in range(0, num_of_hidden_ratings):
            key = random_keys[i]
            hidden_ratings[key] = movie_ratings.pop(key)
        self.movie_ratings = movie_ratings
        self.hidden_ratings = hidden_ratings
