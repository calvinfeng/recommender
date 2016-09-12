require 'csv'
require 'byebug'

def load_movies
  movies = Hash.new
  movies_csv_file = File.read('./ml-latest-small/movies.csv')
  csv = CSV.parse(movies_csv_file, :headers => true)
  csv.each do |row|
    id = row["movieId"].to_i
    title = row["title"]
    movies[id] = {title: title}
  end
  load_user_ratings(movies)
  return movies
end

def load_user_ratings(movies)
  ratings_csv_file = File.read('./ml-latest-small/ratings.csv')
  csv = CSV.parse(ratings_csv_file, :headers => true)
  csv.each do |row|
    user_id = row["userId"].to_i
    movie_id = row["movieId"].to_i
    rating = row["rating"].to_f
    if movies[movie_id][:ratings]
      movies[movie_id][:ratings] << rating
      movies[movie_id][:viewers] << user_id
    else
      movies[movie_id][:ratings] = [rating]
      movies[movie_id][:viewers] = [user_id]
    end
  end
end
