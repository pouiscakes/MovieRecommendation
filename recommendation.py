#!/usr/bin/python
import numpy as np

def get_ratings():
    matrix = []

    i = 1
    for line in open('train.txt'):
        print i, "  \t", line
        user_ratings = line.split('\t')[0:1000]
        matrix.append(user_ratings)
        i += 1

    return matrix

def calculate_cosine_similarity(u1, u2):
    u1 = map(float, u1)
    u2 = map(float, u2)
    return np.dot(u1, u2) / (np.sqrt(np.dot(u1, u1)) * np.sqrt(np.dot(u2, u2)))


ratings = get_ratings()
print " "
print ratings[124][999]  # user 125's rating of 1000th movie
print ratings[199][1]  # user 200's rating of 2nd movie


# print calculate_cosine_similarity(ratings[0], ratings[199])
# print calculate_cosine_similarity(ratings[198], ratings[199])
# print calculate_cosine_similarity(ratings[6], ratings[23])

# # # # find the most similar pairs
# one = 0
# two = 0
# for rating1 in ratings:
#     two = 0
#     for rating2 in ratings:
#         sim = calculate_cosine_similarity(rating1, rating2);
#         if (sim > 0.5) and (sim < .99):
#             print one, " ", two, " ", sim
#         two += 1
#     one += 1

u167 = map(int, ratings[167])
u140 = map(int, ratings[140])

print u167
print u140

