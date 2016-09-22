import csv_loader as loader
import numpy
import pdb
from random import random
from random import sample

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
        preference_vector = []
        while len(preference_vector) < size:
            preference_vector.append(random())
        return preference_vector

class TestUser:
    def __init__(self, user_id, movie_ratings):
        self.id = user_id
        self.theta = self.random_init(8)
        self.process(movie_ratings)

    def random_init(self, size):
        preference_vector = []
        while len(preference_vector) < size:
            preference_vector.append(random())
        return preference_vector

    def process(self, movie_ratings):
        hidden_ratings = dict()
        random_keys = sample(movie_ratings, 2)
        for i in range(0, 2):
            key = random_keys[i]
            hidden_ratings[key] = movie_ratings.pop(key)
        self.movie_ratings = movie_ratings
        self.hidden_ratings = hidden_ratings

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

def content_based_cost(users, movies, l):
    # Content based cost is user-centric
    sq_error = 0
    for user_id in users:
        user = users[user_id]
        for movie_id in user.movie_ratings:
            movie = movies[movie_id]
            sq_error += (movie.hypothesis(user) - float(user.movie_ratings[movie.id]))**2
    sq_error *= 0.5

    regularized_term = 0
    for user_id in users:
        user = users[user_id]
        for k in range(0, len(user.theta)):
            regularized_term += user.theta[k]**2

    return regularized_term*(l/2) + sq_error

def test_cost(users, movies, l):
    sq_error = 0
    for user_id in users:
        user = users[user_id]
        for movie_id in user.hidden_ratings:
            movie = movies[movie_id]
            sq_error += (movie.hypothesis(user) - float(user.hidden_ratings[movie.id]))**2
    sq_error *= 0.5

    regularized_term = 0
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

def derivative_norm(dj):
    norm = 0
    for key in dj:
        norm += numpy.linalg.norm(dj[key])
    return norm

def content_based_gd(movies, users, a, l):
    iteration = 1
    while True:
        print "Iteration #%s - cost: %s" % (iteration, content_based_cost(users, movies, l))
        dj_duser = dict()
        for user_id in users:
            user = users[user_id]
            n = len(user.theta)
            dj_duser[user.id] = []
            for k in range(0, n):
                dj_duser[user.id].append(dj_wrt_user_theta_k(user, movies, l, k))
        print "Iteration #%s - derivative norm => dj_duser: %s" % (iteration, derivative_norm(dj_duser))
        for user_id in dj_duser:
            dj_dtheta = dj_duser[user_id]
            user = users[user_id]
            n = len(user.theta)
            for k in range(0, n):
                user.theta[k] = user.theta[k] - (a*dj_dtheta[k])
        iteration +=1
        if iteration > 2000:
            return True


def gradient_descent(movies, users, a, l):
    iteration = 1
    while True:
        print "Iteration #%s - cost: %s" % (iteration, cost_function(movies, users, l))
        # Compute partial derivatives
        dj_dmovie = dict()
        for movie_id in movies:
            movie = movies[movie_id]
            n = len(movie.feature)
            dj_dmovie[movie.id] = []
            for k in range(0, n):
                dj_dmovie[movie.id].append(dj_wrt_movie_feature_k(movie, users, l, k))
        dj_duser = dict()
        for user_id in users:
            user = users[user_id]
            n = len(user.theta)
            dj_duser[user.id] = []
            for k in range(0, n):
                dj_duser[user.id].append(dj_wrt_user_theta_k(user, movies, l, k))
        print "Iteration #%s - derivative norm => dj_dmovie: %s, dj_duser: %s" % (iteration, derivative_norm(dj_dmovie), derivative_norm(dj_duser))
        # Apply gradient_descent
        for movie_id in dj_dmovie:
            dj_dx = dj_dmovie[movie_id]
            movie = movies[movie_id]
            n = len(movie.feature)
            for k in range(0, n):
                movie.feature[k] = movie.feature[k] - (a*dj_dx[k])
        for user_id in dj_duser:
            dj_dtheta = dj_duser[user_id]
            user = users[user_id]
            n = len(user.theta)
            for k in range(0, n):
                user.theta[k] = user.theta[k] - (a*dj_dtheta[k])
        iteration +=1
        if iteration > 2000:
            return True

movie_set = './gd-10-movies/movies.csv'
rating_train_set = './gd-10-movies/ratings_train.csv'
rating_cv_set = './gd-10-movies/ratings_cv.csv'
rating_test_set = './gd-10-movies/ratings_test.csv'

train_set_movies = loader.load_movies(movie_set, rating_train_set)
train_set_users = loader.load_users(rating_train_set)
cv_set_users = loader.load_users(rating_cv_set)
test_set_users = loader.load_users(rating_test_set)

movies = dict()
for movie_id in train_set_movies:
    movies[movie_id] = Movie(movie_id,train_set_movies[movie_id]["title"], train_set_movies[movie_id]["viewers"])

train_users = dict()
for user_id in train_set_users:
    train_users[user_id] = User(user_id, train_set_users[user_id])

cv_users = dict()
for user_id in cv_set_users:
    if len(cv_set_users[user_id]) > 5:
        cv_users[user_id] = TestUser(user_id, cv_set_users[user_id])

regularized_factor = 0.05
gradient_descent(movies, train_users, 0.0015, regularized_factor)
content_based_gd(movies, cv_users, 0.0015, regularized_factor)
print "Movie train cost: %s" %cost_function(movies, train_users, regularized_factor)
print "Train cost: %s" % content_based_cost(cv_users, movies, regularized_factor)
print "CV cost: %s" % test_cost(cv_users, movies, regularized_factor)
pdb.set_trace()
print "Done"
