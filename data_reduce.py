import csv_loader
import pdb
import csv

MOVIE_SET = './ml-latest/movies.csv'
RATING_SET = './ml-latest/ratings.csv'
LINKS_SET = './ml-latest/links.csv'

def reduce_movies_file(movie_set):
    movies_csv = open(MOVIE_SET)
    csv_reader = csv.reader(movies_csv)
    resized_movies_csv = open('./ml-latest-med/movies.csv', 'wt')
    csv_writer = csv.writer(resized_movies_csv)
    csv_writer.writerow(('movieId', 'title', 'genres'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and row[0] in movie_set:
            csv_writer.writerow((row[0], row[1], row[2]))
            write_count += 1
    print "Wrote %s items to movies.csv" % write_count


def reduce_ratings_file(user_set):
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    resized_ratings_csv = open('./ml-latest-med/ratings.csv', 'wt')
    csv_writer = csv.writer(resized_ratings_csv)
    csv_writer.writerow(('userId', 'movieId', 'rating', 'timestamp'))
    write_count = 0
    movie_id_set = set()
    for row in csv_reader:
        if row[0].isdigit() and row[0] in user_set:
            csv_writer.writerow((row[0], row[1], row[2], row[3]))
            movie_id_set.add(row[1])
            write_count += 1

    print "Wrote %s items to ratings.csv" % write_count
    return movie_id_set

def reduce_links_file(movie_set):
    links_csv = open(LINKS_SET)
    csv_reader = csv.reader(links_csv)
    resized_links_csv = open('./ml-latest-med/links.csv', 'wt')
    csv_writer = csv.writer(resized_links_csv)
    csv_writer.writerow(('movieId', 'imdbId', 'tmdbId'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and row[0] in movie_set:
            csv_writer.writerow((row[0], row[1], row[2]))
            write_count += 1
    print "Wrote %s items to links.csv" % write_count


full_movies = csv_loader.load_movies(MOVIE_SET, RATING_SET)
full_users = csv_loader.load_users(RATING_SET)

user_id_set = set()
for i in range(1, 100000):
    user_id = str(i)
    if len(full_users[user_id]) >= 50 and len(full_users[user_id]) <= 100:
        user_id_set.add(str(user_id))
    if len(user_id_set) == 5000:
         break
# There are 14839 people (who rated between 50 and 100 movies) in 100,000 people
print "user_set length: %s" % len(user_id_set)
movie_id_set = reduce_ratings_file(user_id_set)
print "movie_set length: %s" % len(movie_id_set)
reduce_movies_file(movie_id_set)
reduce_links_file(movie_id_set)
