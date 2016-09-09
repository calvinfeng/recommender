import csv
import pdb

def load_movies():
    movies = dict()
    movies_csv = open('./ml-latest-small/movies.csv')
    csv_reader = csv.reader(movies_csv)
    for row in csv_reader:
        if row[0].isdigit():
            movie_id = row[0]
            movie_title = row[1]
            movies[movie_id] = movie_title
    return movies

def load_user_ratings():
    
