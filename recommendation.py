#!/usr/bin/python
import numpy as np
import heapq
import math


#  return a 2D matrix of user ratings: l[user][rating]
def get_ratings():
    matrix = []
    i = 1

    for line in open('train.txt'):
        # print i, "  \t", line
        user_ratings = line.split('\t')[0:1000]
        matrix.append(user_ratings)
        i += 1
    return matrix


#  add the test file to the ratings and return new ratings
def add_test(testfile, ratings):
    test = open(testfile, 'r')
    rows = []
    i = 0
    for line in test:
        rows.append(line.split(' ')[0:3])
        i += 1
    i = 0
    for i in range(0, len(rows)):
        rows[i][2] = rows[i][2][0]
    # print rows

    for index in range(0,100):
        ratings.append(['0'] * 1000)

    for row in rows:
        user = int(row[0]) - 1
        if testfile == 'test10.txt':
            user -= 100
        if testfile == 'test20.txt':
            user -= 200
        movie = int(row[1]) - 1
        rating = row[2]
        # print user, " ", movie, " ", rating
        ratings[user][movie] = rating

    return ratings


#  return cosine similarity between two vectors
def calculate_cosine_similarity(v1, v2):
    v1 = map(float, v1)
    v2 = map(float, v2)
    # return np.dot(v1, v2) / (np.sqrt(np.dot(v1, v1)) * np.sqrt(np.dot(v2, v2)))

    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        if x > 0 and y > 0:
            # print str(x) + " " + str(y)
            sumxx += x*x
            sumyy += y*y
            sumxy += x*y
        # print str(sumxy) +  " / " + str(math.sqrt(sumxx * sumyy))
    try:
        result = sumxy/math.sqrt(sumxx*sumyy)
        if result == 1.0:
            return .75
        return result

    except ZeroDivisionError:
        return 0.5



#  return indexes of the nearest n neighbors based on given similarity algorithm
def get_neighbors(n, index, ratings, similarity):
    if 299 < index < 400:
        index -= 100
    elif 399 < index < 500:
        index -= 200

    sim_list = []
    for r1 in range(0, len(ratings)):
        if r1 != index:
            sim = similarity(ratings[r1], ratings[index])
            sim_list.append(sim)

    indexes = sorted(range(len(sim_list)), key=lambda x: sim_list[x])[-n:]
    indexes.reverse()
    print "cos sims: ", heapq.nlargest(n, (s for s in sim_list))
    return indexes


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
    return int(round(avg))
    # return avg


def write_result(ratings, inFile, outFile):
    input = open(inFile, 'r')
    rows = []
    modified_rows = []

    i = 0
    for line in input:
        rows.append(line.split(' ')[0:3])  # split line
        i += 1
    i = 0
    for i in range(0, len(rows)):
        rows[i][2] = rows[i][2][0]  # remove extra text after rating
    # print rows

    at_user = 0

    for i in range(0, len(rows)):
        user = int(rows[i][0]) - 1
        movie = int(rows[i][1]) - 1
        rating = rows[i][2]

        if movie == 999: ### THIS IS A HACK BC OUT OF BOUNDS??
            rows[i][2] = 4
            print "modified: ", rows[i]
            modified_rows.append(rows[i])

        elif rating == '0':
            # print "rating is 0"
            if at_user != user:
                neighbors = get_neighbors(20, user, ratings, similarity=calculate_cosine_similarity)
                print neighbors
                at_user = user;
            rows[i][2] = str(weighted_average(movie, neighbors, ratings))
            print "modified: ", rows[i]
            modified_rows.append(rows[i])

    f = open(outFile, 'w')
    # rows = sorted(rows, key=lambda x: (x[0], -x[1]))
    for row in modified_rows:
        # print row
        line = str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + '\n'
        f.write(line)  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it

#  main
inFile = 'test5.txt'
outFile = 'result5.txt'
ratings = get_ratings()
ratings = add_test(inFile, ratings)
# i = 0
# while i < 300:
#     print i, " ", ratings[i]
#     i += 1

# neighbors = get_neighbors(20, 217, ratings, similarity=calculate_cosine_similarity)
# print neighbors

write_result(ratings, inFile, outFile);

# n = 10
# sim_list = []
# for r in ratings:
#     sim_list.append(calculate_cosine_similarity(ratings[200], r))
# indexes = sorted(range(len(sim_list)), key=lambda x: sim_list[x])[-n:]
# indexes.reverse()
# print indexes
# print "cos sims: ", heapq.nlargest(n, (s for s in sim_list))
#
# print ratings[200]
# print ratings[89]

# movie = 999
# for neighbor in neighbors:
#     print ratings[neighbor]#[movie]
#
# print weighted_average(movie, neighbors, ratings)
#
# testx = 14
# print "index ", testx
# print ratings[testx][236]
# print ratings[testx][305]
# print ratings[testx][360]
# print ratings[testx][474]
# print ratings[testx][933]
# testx = 67
# print "index ", testx
# print ratings[testx][236]
# print ratings[testx][305]
# print ratings[testx][360]
# print ratings[testx][474]
# print ratings[testx][933]
# testx = 200
# print "index ", testx
# print ratings[testx][236]
# print ratings[testx][305]
# print ratings[testx][360]
# print ratings[testx][474]
# print ratings[testx][933]
# testx = 243
# print "index ", testx
# print ratings[testx][236]
# print ratings[testx][305]
# print ratings[testx][360]
# print ratings[testx][474]
# print ratings[testx][933]
# print ratings[244]

# sum1 = 0
# count1 = 0
# for i in range(0,999):
#     w = weighted_average(i,neighbors, ratings) #  make it not round to int
#     if(w != 0):
#         sum1 += w
#         count1 += 1
# avg1 = sum1 / count1
# print sum1
# print count1
# print avg1

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
