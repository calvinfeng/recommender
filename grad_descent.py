import csv_loader as loader
import numpy
import pdb
import math
import csv
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

# class User:
#     def __init__(self, user_id, movie_ratings):
#         self.id = user_id
#         self.movie_ratings = movie_ratings
#         self.theta = self.random_init(8)
#
#     def random_init(self, size):
#         preference_vector = []
#         while len(preference_vector) < size:
#             preference_vector.append(random())
#         return preference_vector

class User:
    def __init__(self, user_id, movie_ratings):
        self.id = user_id
        self.theta = self.random_init(8)
        self.process(movie_ratings)

    def random_init(self, size):
        # Give User a bias term, which is 1
        preference_vector = [1]
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
#===============================================================================
def cost_function(movies, users, l):
    sq_error = 0
    m = 0
    for movie_id in movies:
        movie = movies[movie_id]
        viewers = movie.viewers
        for user_id in viewers:
            user = users[user_id]
            if user.movie_ratings.get(movie.id):
                sq_error += (movie.hypothesis(user) - float(user.movie_ratings[movie.id]))**2
                m += 1
    sq_error *= (0.5/m)

    regularized_term = 0
    for movie_id in movies:
        movie = movies[movie_id]
        for k in range(0, len(movie.feature)):
            regularized_term += movie.feature[k]**2

    for user_id in users:
        user = users[user_id]
        for k in range(0, len(user.theta)):
            regularized_term += user.theta[k]**2
    regularized_term *= (0.5*l/m)

    return regularized_term + sq_error

def content_based_cost(users, movies, l):
    # Content based cost is user-centric
    sq_error = 0
    m = 0
    for user_id in users:
        user = users[user_id]
        for movie_id in user.movie_ratings:
            movie = movies[movie_id]
            sq_error += (movie.hypothesis(user) - float(user.movie_ratings[movie.id]))**2
            m += 1
    sq_error *= (0.5/m)

    regularized_term = 0
    for user_id in users:
        user = users[user_id]
        for k in range(0, len(user.theta)):
            regularized_term += user.theta[k]**2
    regularized_term *= (0.5*l/m)

    return regularized_term + sq_error

# Root Mean Squared Error
def cv_rmse(users, movies):
    sq_error = 0
    m = 0
    for user_id in users:
        user = users[user_id]
        for movie_id in user.hidden_ratings:
            movie = movies[movie_id]
            sq_error += (movie.hypothesis(user) - float(user.hidden_ratings[movie.id]))**2
            m += 1
    return math.sqrt(sq_error/m)

def train_rmse(users, movies):
    sq_error = 0
    m = 0
    for user_id in users:
        user = users[user_id]
        for movie_id in user.movie_ratings:
            movie = movies[movie_id]
            sq_error += (movie.hypothesis(user) - float(user.movie_ratings[movie_id]))**2
            m += 1
    return math.sqrt(sq_error/m)

#===============================================================================
#=============================Derivatives=======================================
# wrt = with respect to
def dj_wrt_movie_feature_k(movie, users, l, k):
    derivative_sum = 0
    m = 0
    for user_id in movie.viewers:
        user = users[user_id]
        if user.movie_ratings.get(movie.id):
            temp = movie.hypothesis(user) - float(user.movie_ratings[movie.id])
            temp *= user.theta[k]
            derivative_sum += temp
            m += 1

    if m == 0:
        return derivative_sum + l*movie.feature[k]
    else:
        return (derivative_sum/m) + (l*movie.feature[k]/m)

# wrt = with respect to
def dj_wrt_user_theta_k(user, movies, l, k):
    derivative_sum = 0
    m = 0
    for movie_id in user.movie_ratings:
        movie = movies[movie_id]
        temp = (movie.hypothesis(user) - float(user.movie_ratings[movie_id]))
        temp *= movie.feature[k]
        derivative_sum += temp
        m += 1
    if m == 0:
        return derivative_sum + (l*user_theta[k])
    else:
        return (derivative_sum/m) + (l*user.theta[k]/m)

def dj_wrt_user_theta_k0(user, movies):
    derivative_sum = 0
    m = 0
    for movie_id in user.movie_ratings:
        movie = movies[movie_id]
        temp = (movie.hypothesis(user) - float(user.movie_ratings[movie_id]))
        temp *= movie.feature[0]
        derivative_sum += temp
        m += 1
    if m == 0:
        return derivative_sum
    else:
        return (derivative_sum/m)

#===============================================================================
#========================Stochastic Derivatives=================================

def stochastic_dj_wrt_movie_feature_k(movie, users, l, k):
    derivative_sum = 0
    batch_size = 1
    if len(movie.viewers) > 0:
        user_id_list = sample(movie.viewers, batch_size)
        for user_id in user_id_list:
            user = users[user_id]
            temp = movie.hypothesis(user) - float(user.movie_ratings[movie.id])
            temp *= user.theta[k]
            derivative_sum += temp
    return (derivative_sum/batch_size) + (l*movie.feature[k]/batch_size)

def stochastic_dj_wrt_user_theta_k(user, movies, l, k):
    derivative_sum = 0
    batch_size = 1
    if len(user.movie_ratings) > 0:
        movie_id_list = sample(user.movie_ratings, batch_size)
        for movie_id in movie_id_list:
            movie = movies[movie_id]
            temp = (movie.hypothesis(user) - float(user.movie_ratings[movie_id]))
            temp *= movie.feature[k]
            derivative_sum += temp
    return (derivative_sum/batch_size) + (l*user.theta[k]/batch_size)

def derivative_norm(dj):
    norm = 0
    for key in dj:
        norm += numpy.linalg.norm(dj[key])
    return norm

#===============================================================================
def content_based_grad_descent(movies, users, a, l):
    iteration = 0
    while True:
        if iteration%100 == 0:
            print "Iteration #%s - cost: %s" % (iteration, content_based_cost(users, movies, l))
        dj_duser = dict()
        for user_id in users:
            user = users[user_id]
            n = len(user.theta)
            dj_duser[user.id] = []
            for k in range(0, n):
                if k == 0:
                    dj_duser[user.id].append(dj_wrt_user_theta_k0(user, movies))
                else:
                    dj_duser[user.id].append(dj_wrt_user_theta_k(user, movies, l, k))
        if iteration%100 == 0:
            print "Iteration #%s - derivative norm => dj_duser: %s" % (iteration, derivative_norm(dj_duser))
        for user_id in dj_duser:
            dj_dtheta = dj_duser[user_id]
            user = users[user_id]
            n = len(user.theta)
            for k in range(0, n):
                user.theta[k] = user.theta[k] - (a*dj_dtheta[k])
        iteration +=1
        if iteration > 5000:
            return True

def batch_gradient_descent(movies, users, a, l):
    iteration = 0
    log = []
    while True:
        if iteration%50 == 0:
            record = []
            cost = cost_function(movies, users, l)
            training_error = train_rmse(users, movies)
            cv_error = cv_rmse(users, movies)
            print "Iteration #%s - cost: %s" % (iteration, cost)
            record.append(iteration)
            record.append(cost)
            record.append(training_error)
            record.append(cv_error)
            log.append(record)
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
        if iteration > 1500:
            return log

def stochastic_gradient_descent(movies, users, a, l):
    iteration = 0
    while True:
        print "Iteration #%s - cost: %s" % (iteration, cost_function(movies, users, l))
        # Compute partial derivatives
        dj_dmovie = dict()
        for movie_id in movies:
            movie = movies[movie_id]
            n = len(movie.feature)
            dj_dmovie[movie.id] = []
            for k in range(0, n):
                dj_dmovie[movie.id].append(stochastic_dj_wrt_movie_feature_k(movie, users, l, k))
        dj_duser = dict()
        for user_id in users:
            user = users[user_id]
            n = len(user.theta)
            dj_duser[user.id] = []
            for k in range(0, n):
                dj_duser[user.id].append(stochastic_dj_wrt_user_theta_k(user, movies, l, k))
        # Update feature and preference vectors
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
        if iteration > 1000:
            return True

def write_feature_to_csv(movies):
    feature_csv = open('./knn-10k-users/features.csv', 'wt')
    csv_writer = csv.writer(feature_csv)
    header = ['movieId']
    for k in range(0, 8):
        header.append("x%s" % k)
    csv_writer.writerow(header)
    for movie_id in movies:
        movie = movies[movie_id]
        csv_writer.writerow([movie_id] + movie.feature)
    return True

def write_rmse_to_csv(log):
    log_csv = open("./knn-10k-users/log.csv", 'wt')
    csv_writer = csv.writer(log_csv)
    header = ['iteration','costFunction', 'trainingRmse', 'cvRmse']
    csv_writer.writerow(header)
    for k in range(0, len(log)):
        csv_writer.writerow(log[k])
    return True

movie_set = './knn-10k-users/movies.csv'
rating_set = './knn-10k-users/ratings.csv'
# rating_cv_set = './gd-10-movies/ratings_cv.csv'
# rating_test_set = './gd-10-movies/ratings_test.csv'

movie_set = loader.load_movies(movie_set, rating_set)
user_set = loader.load_users(rating_set)
# cv_set_users = loader.load_users(rating_cv_set)
# test_set_users = loader.load_users(rating_test_set)

movies = dict()
for movie_id in movie_set:
    movies[movie_id] = Movie(movie_id, movie_set[movie_id]["title"], movie_set[movie_id]["viewers"])

users = dict()
for user_id in user_set:
    users[user_id] = User(user_id, user_set[user_id])

learning_rate = 0.15
regularized_factor = 0.1
print "Train RMSE: %s" % train_rmse(users, movies)
print "CV RMSE: %s" % cv_rmse(users, movies)
log = batch_gradient_descent(movies, users, learning_rate, regularized_factor)
print "(After gradient_descent) Train RMSE: %s" % train_rmse(users, movies)
print "(After gradient_descent) CV RMSE: %s" % cv_rmse(users, movies)
write_rmse_to_csv(log)
for user_id in users:
    user = users[user_id]
    for movie_id in user.hidden_ratings:
        print "Title: %s" % movies[movie_id].title
        print "=> # of viewers: %s, rating: %s, prediction: %s" % (len(movies[movie_id].viewers), user.hidden_ratings[movie_id], movies[movie_id].hypothesis(user))
pdb.set_trace()
write_feature_to_csv(movies)
print "Done"
