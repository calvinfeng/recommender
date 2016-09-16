import csv_loader

def reduce_set(movies):
    reduced_set = dict()
    for movie_id in movies:
        if movies[movie_id].get("ratings") and len(movies[movie_id]["ratings"]) >= 50:
            #print movies[movie_id]["title"]
            reduced_set[movie_id] = True
    print "Length: %s" % len(reduced_set)
    return reduced_set

def reduce_ratings_file(movie_set):
    ratings_csv = open(RATING_SET)
    csv_reader = csv.reader(ratings_csv)
    resized_ratings_csv = open('./ml-data/ratings.csv', 'wt')
    csv_writer = csv.writer(resized_ratings_csv)
    csv_writer.writerow(('userId', 'movieId', 'rating', 'timestamp'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and int(row[0]) <= 10000 and movie_set.get(row[1]):
            csv_writer.writerow((row[0], row[1], row[2], row[3]))
            write_count += 1
    print "Wrote %s items to ratings.csv" % write_count

def reduce_movie_file(movie_set):
    movies_csv = open(MOVIE_SET)
    csv_reader = csv.reader(movies_csv)
    resized_movies_csv = open('./ml-data/movies.csv', 'wt')
    csv_writer = csv.writer(resized_movies_csv)
    csv_writer.writerow(('movieId', 'title', 'genres'))
    write_count = 0
    for row in csv_reader:
        if row[0].isdigit() and movie_set.get(row[0]):
            csv_writer.writerow((row[0], row[1], row[2]))
            write_count += 1
    print "Wrote %s items to movies.csv" % write_count

# movies = load_movies()
# movies_with_50_reviews = reduce_set(movies) # Movies with at least 50 reviews coming from 20,000 users
# reduce_ratings_file(movies_with_50_reviews)
# reduce_movie_file(movies_with_50_reviews)
