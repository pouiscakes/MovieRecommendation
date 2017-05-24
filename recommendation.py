#!/usr/bin/python
import numpy as np


#  return a 2D matrix of user ratings: l[user][rating]
def get_ratings():
    matrix = []
    i = 1

    for line in open('train.txt'):
        print i, "  \t", line
        user_ratings = line.split('\t')[0:1000]
        matrix.append(user_ratings)
        i += 1
    return matrix


#  return cosine similarity between two vectors
def calculate_cosine_similarity(u1, u2):
    u1 = map(float, u1)
    u2 = map(float, u2)
    return np.dot(u1, u2) / (np.sqrt(np.dot(u1, u1)) * np.sqrt(np.dot(u2, u2)))


#  return indexes of the nearest n neighbors based on given similarity algorithm
def get_neighbors(n, index, ratings, similarity):
    sim_list = []
    for r1 in range(0, len(ratings)):
        if r1 != index:
            sim = similarity(ratings[r1], ratings[index])
            sim_list.append(sim)

    indexes = sorted(range(len(sim_list)), key=lambda x: sim_list[x])[-n:]
    indexes.reverse()
    return indexes
    # print "cos sims: ", heapq.nlargest(n, (s for s in sim_list))


def weighted_average(movie, neighbors, ratings):
    sum = 0
    count = 0
    for neighbor in neighbors:
        score = map(float, ratings[neighbor][movie])[0]
        if score > 0:
            sum += score
            count += 1
    if count == 0:
        return 4
    avg = sum / count
    return avg

#  main
ratings = get_ratings()
neighbors = get_neighbors(10, 17, ratings, similarity=calculate_cosine_similarity)
print neighbors



movie = 992
for neighbor in neighbors:
    print ratings[neighbor]#[movie]

print weighted_average(movie, neighbors, ratings)





# print " "
# print ratings[124][999]  # user 125's rating of 1000th movie
# print ratings[199][1]  # user 200's rating of 2nd movie

# print calculate_cosine_similarity(ratings[0], ratings[199])
# print calculate_cosine_similarity(ratings[198], ratings[199])
# print calculate_cosine_similarity(ratings[6], ratings[23])

# # # # find the most similar neighbors
# sim_list = []
# for r1 in range(0, len(ratings)):
#     for r2 in range(r1 + 1, len(ratings)):
#         sim = calculate_cosine_similarity(ratings[r1], ratings[r2])
#         sim_list.append(sim)
#
# print "sim_list: ", sim_list
# print heapq.nlargest(3, (s for s in sim_list))
