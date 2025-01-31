import csv_loader
import pdb
import csv

def create_ratings_train_set(movie_set):
    csv_reader = csv.reader(open(RATING_SET))
    csv_writer = csv.writer(open('./gd-10-movies/ratings_train.csv', 'wt'))
    csv_writer.writerow(('userId', 'movieId', 'rating', 'timestamp'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and row[1] in movie_set and int(row[0]) < 5000:
            csv_writer.writerow((row[0], row[1], row[2], row[3]))
            write_count += 1
    print "Wrote %s items to ratings_train.csv" % write_count

def create_ratings_test_set(movie_set):
    csv_reader = csv.reader(open(RATING_SET))
    # Create a cross validation data set
    cv_writer = csv.writer(open('./gd-10-movies/ratings_cv.csv', 'wt'))
    cv_writer.writerow(('userId', 'movieId', 'rating', 'timestamp'))
    # Create a test data set
    test_writer = csv.writer(open('./gd-10-movies/ratings_test.csv', 'wt'))
    test_writer.writerow(('userId', 'movieId', 'rating', 'timestamp'))

    cv_count = 0
    test_count = 0
    for row in csv_reader:
        if row[0].isdigit() and row[1] in movie_set and int(row[0]) >= 5000 and int(row[0]) < 7500:
            cv_writer.writerow((row[0], row[1], row[2], row[3]))
            cv_count += 1
        elif row[0].isdigit() and row[1] in movie_set and int(row[0]) >= 7500 and int(row[0]) < 10000:
            test_writer.writerow((row[0], row[1], row[2], row[3]))
            test_count += 1

    print "Wrote %s items to ratings_cv.csv" % cv_count
    print "Wrote %s items to ratings_test.csv" % test_count

def reduce_movies_file(movie_set):
    movies_csv = open(MOVIE_SET)
    csv_reader = csv.reader(movies_csv)
    resized_movies_csv = open('./gd-10-movies/movies.csv', 'wt')
    csv_writer = csv.writer(resized_movies_csv)
    csv_writer.writerow(('movieId', 'title', 'year', 'genres'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and row[0] in movie_set:
            movie_id = row[0]
            title = row[1].strip()
            year = title[len(title) - 5: len(title) - 1]
            genres = row[2]
            title = title[:len(title) - 6].strip()
            csv_writer.writerow((movie_id, title, year, genres))
            write_count += 1
    print "Wrote %s items to movies.csv" % write_count

def reduce_links_file(movie_set):
    links_csv = open(LINKS_SET)
    csv_reader = csv.reader(links_csv)
    resized_links_csv = open('./gd-10-movies/links.csv', 'wt')
    csv_writer = csv.writer(resized_links_csv)
    csv_writer.writerow(('movieId', 'imdbId', 'tmdbId'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and row[0] in movie_set:
            csv_writer.writerow((row[0], "tt" + row[1], row[2]))
            write_count += 1
    print "Wrote %s items to links.csv" % write_count

def reduce_ratings_file(movie_set):
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    resized_ratings_csv = open('./gd-10-movies/ratings.csv', 'wt')
    csv_writer = csv.writer(resized_ratings_csv)
    csv_writer.writerow(('userId', 'movieId', 'rating', 'timestamp'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and row[1] in movie_set:
            csv_writer.writerow((row[0], row[1], row[2], row[3]))
            write_count += 1

    print "Wrote %s items to ratings.csv" % write_count

MOVIE_SET = './ml-latest/movies.csv'
RATING_SET = './ml-latest/ratings.csv'
LINKS_SET = './ml-latest/links.csv'

knn_movie_set = './knn-10k-users/movies.csv'
knn_ratings_set = './knn-10k-users/ratings.csv'
knn_links_set = './knn-10k-users/links.csv'

full_movies = csv_loader.load_movies(knn_movie_set, knn_ratings_set)
full_users = csv_loader.load_users(knn_ratings_set)
count = 0
for movie_id in full_movies:
    if len(full_movies[movie_id]["ratings"]) > 0 and full_movies[movie_id]["year"] == '2015':
        count += 1
        print "Title: %s, number of viewers: %s" % (full_movies[movie_id]["title"],  len(full_movies[movie_id]["ratings"]))
pdb.set_trace()
movie_id_set = set()
for i in range(1, len(full_movies)):
    movie_id = str(i)
    if full_movies.get(movie_id):
        if len(full_movies[movie_id]["ratings"]) >= 20000:
            movie_id_set.add(movie_id)
    if len(movie_id_set) == 10:
         break

print "Items in movie_id_set: %s" % len(movie_id_set)
reduce_movies_file(movie_id_set)
reduce_links_file(movie_id_set)
create_ratings_train_set(movie_id_set)
create_ratings_test_set(movie_id_set)
