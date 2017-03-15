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

        if len(movies_seen_by_both) >= 5:
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
    def __init__(self, movie_id, movie_title, user_ratings, viewers):
        self.id = movie_id
        self.title = movie_title
        self.avg_rating = Movie.compute_avg_ratings(user_ratings)
        self.num_of_ratings = len(user_ratings)
        self.ratings = user_ratings
        self.viewers = viewers

    @staticmethod
    def compute_avg_ratings(user_ratings):
        avg_rating = 0
        for rating in user_ratings:
            avg_rating += float(rating)
        avg_rating = avg_rating/len(user_ratings)
        return avg_rating

def predict_rating(user, movie, users_data):
    neighbors = movie.viewers
    score = 0
    sim_norm = 0
    for neighbor_id in neighbors:
        neighbor = User(neighbor_id, users_data[neighbor_id])
        sim = User.sim(user, neighbor)
        if sim > 0.50:
            score += sim*(float(neighbor.ratings[movie.id]) - float(neighbor.avg_rating))
            sim_norm += abs(sim)
    if sim_norm == 0:
        return "Insufficient information"
    else:
        return user.avg_rating + score/sim_norm


# my_ratings = {'2959': 4.5, '58559': 3.5, '2571': 4.5, '79132': 5.0, '2329': 4.0, '92259': 2.0, '5971': 3.0}
# new_user = User(None, my_ratings)
# for movie in movies:
#     if not new_user.ratings.get(movie.id):
#         p_rating = predict_rating(new_user, movie, users_data)
#         print "Title: %s with Avg: %s, and Pred: %s" % (movie.title, movie.avg_rating, p_rating)
