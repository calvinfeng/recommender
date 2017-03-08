# Project: Recommender System
# Author(s): Calvin Feng

from movie import Movie
from user import User
from data_reducer import DataReducer
from progress import Progress

class KNearest:

    def __init__(self, movie_csv_filepath, rating_csv_filepath, link_csv_filepath):
        reducer = DataReducer(movie_csv_filepath, rating_csv_filepath, link_csv_filepath):

        latent_factor_length = 0

        self.movies = dict()
        for movie_id in reducer.movies:
            movie = self.reducer.movies[movie_id]
            self.movies[movie_id] = Movie(movie_id, movie['title'], movie['user_ratings'], latent_factor_length)

        self.users = dict()
        for user_id in reducer.users:
            user = self.reducer.users[user_id]
            self.users[user_id] = User(user_id, user['movie_ratings'], latent_factor_length, True)

    def hypothesis(self, user, movie):
        
