import random
import sys
import time

import numpy as np
import pandas as pd

# Initializing global variables
data_cluster_map = {}
cluster_data_map = {}
input_file = sys.argv[1]
num_clusters = int(sys.argv[2])
output_file_name = sys.argv[3]

# Removing categorical attribute
df = pd.read_csv(input_file, sep=',', error_bad_lines=False, header=None)
df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)

for i in range(len(df)):
    data_cluster_map.update({i: 0})

for i in range(num_clusters):
    cluster_data_map.update({i: set()})


# Finds the average of a list of tuples(vector)
def tuple_average(tup_list):
    return tuple([np.average([tup[idx] for tup in tup_list]) for idx in range(len(tup_list[0]))])


# Finds the euclidean distance of two tuples(vector)
def euclidean_dist(tup1, tup2):
    return np.sqrt(sum([(tup1[idx] - tup2[idx]) ** 2 for idx in range(len(tup1))]))


# Clusters the dataset into k clusters
def k_means(k):
    centroids_index = random.sample(range(len(df)), k)
    centroids = [tuple(df.loc[index]) for index in centroids_index]
    change = True
    count = 0
    sum_squared_error = 0
    silhouette_coeff = 0
    while change:
        change = False
        for idx in range(len(df)):
            dist_from_centroids = [euclidean_dist(tuple(df.loc[idx]), centroid) for centroid in centroids]
            cluster_idx = dist_from_centroids.index(min(dist_from_centroids))

            # Updating data -> cluster map
            old_cluster_idx = data_cluster_map.get(idx)
            if cluster_idx != old_cluster_idx:
                change = True  # The clusters have changed
                data_cluster_map.update({idx: cluster_idx})

            # Updating cluster -> data map
            # Removing from old cluster
            if count >= 1:
                data_in_cluster = cluster_data_map.get(old_cluster_idx)
                data_in_cluster.remove(idx)
                cluster_data_map.update({old_cluster_idx: data_in_cluster})
            # Adding to new cluster
            data_in_cluster = cluster_data_map.get(cluster_idx)
            data_in_cluster.add(idx)
            cluster_data_map.update(
                {cluster_idx: data_in_cluster})

        # Updating centroids
        for idx in range(len(centroids)):
            centroids[idx] = tuple_average([df.loc[cluster_data] for cluster_data in cluster_data_map.get(idx)])

        count += 1

    # Calculating sum squared error and silhouette coefficient
    for idx in range(len(df)):
        sum_squared_error += euclidean_dist(tuple(df.loc[idx]), centroids[data_cluster_map[idx]]) ** 2
        a = sum(
            [euclidean_dist(tuple(df.loc[idx]), tuple(df.loc[neighbor])) for neighbor in
             cluster_data_map[data_cluster_map[idx]]]) / (len(cluster_data_map[data_cluster_map[idx]]) - 1)
        b = min([sum(
            [euclidean_dist(tuple(df.loc[idx]), tuple(df.loc[distant])) for distant in cluster_data_map[idx2]]) / len(
            cluster_data_map[idx2]) for idx2 in range(k) if idx2 != data_cluster_map[idx]])
        silhouette_coeff += (b - a) / max(a, b)

    silhouette_coeff = silhouette_coeff / len(df)

    return sum_squared_error, silhouette_coeff


start_time = time.time()
(sse, sc) = k_means(num_clusters)
print("--- %s seconds ---" % (time.time() - start_time))

for cluster in cluster_data_map:
    print(len(cluster_data_map[cluster]))
print("SSE: ", sse)
print("sc: ", sc)
output_file = open(output_file_name, 'w')
for i in range(len(df)):
    output_file.write(str(data_cluster_map.get(i)))
    output_file.write('\n')
output_file.write("SSE: %f \t SC: %f" % (sse, sc))
output_file.close()
