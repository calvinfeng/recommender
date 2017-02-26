
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
