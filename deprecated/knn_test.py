from k_nearest import User
from k_nearest import Movie
from k_nearest import predict_rating
import csv_loader as loader
import pdb

SMALL_MOVIE_SET = './ml-latest-small/movies.csv'
SMALL_RATING_SET = './ml-latest-small/ratings.csv'

MOVIE_SET = './ml-latest/movies.csv'
RATING_SET = './ml-latest/ratings.csv'

med_rating_csv = './ml-latest-med/ratings.csv'
med_movie_csv = './ml-latest-med/movies.csv'
med_link_csv = './ml-latest-med/links.csv'

train_set_movies = loader.load_movies(med_movie_csv, med_rating_csv)
train_set_users = loader.load_users(med_rating_csv)
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

movies = []
for movie_id in train_set_movies:
    if train_set_movies[movie_id].get("viewers") and len(train_set_movies[movie_id]['viewers']) > 300:
        movies.append(Movie(movie_id, train_set_movies[movie_id]['title'], train_set_movies[movie_id]['ratings'], train_set_movies[movie_id]['viewers']))
print "Number of movies with significant number of reviews: %s \n" % len(movies)
movies = quick_sort(movies)
test_set_users = loader.load_users(RATING_SET)
# pdb.set_trace()
prediction_count = 0
accurate_count = 0
for i in range(0, 100):
    print "Title: %s" % (movies[i].title)
    for j in range(100001, 102000):
        user_id = str(j)
        if test_set_users[user_id].get(movies[i].id) and len(test_set_users[user_id]) > 20 and len(test_set_users[user_id]) < 100:
            # Initialize test subject
            actual_rating = test_set_users[user_id].pop(movies[i].id)
            test_user = User(user_id, test_set_users[user_id])
            # Compute predicted rating for test subject
            predicted_rating = predict_rating(test_user, movies[i], train_set_users)
            print "User #%s has rated %s movies: predicted rating = %s, actual rating = %s" % (user_id, len(test_user.ratings) + 1, predicted_rating, actual_rating)
            if isinstance(predicted_rating, float):
                prediction_count += 1
                discrepancy = abs(predicted_rating - float(actual_rating))
                if discrepancy <= 0.50 :
                    accurate_count += 1

print "Total number of predictions: %s" % prediction_count
print "Number of prediction with good accuracy: %s" % accurate_count
