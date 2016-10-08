import csv
import pdb

def load_features(file_location):
    features = dict()
    features_csv = open(file_location)
    csv_reader = csv.reader(features_csv)
    for row in csv_reader:
        if row[0].isdigit():
            movie_id = row[0]
            vector = []
            for i in range(1,9):
                vector.append(row[i])
            features[movie_id] = vector
    return features

old_features = load_features('./knn-5k-users/features.csv')
new_features = load_features('./knn-5k-users/updated_features.csv')

# update_csv = open('./knn-5k-users/updated_features.csv', 'wt')
# csv_writer = csv.writer(update_csv)
# header = ['movieId']
# for k in range(0, 8):
#     header.append("x%s" % k)
# csv_writer.writerow(header)

for movie_id in old_features:
    if new_features.get(movie_id):
        # row = [movie_id] + new_features[movie_id]
        # csv_writer.writerow(row)
    else:
        # row = [movie_id] + old_features[movie_id]
        # csv_writer.writerow(row)
