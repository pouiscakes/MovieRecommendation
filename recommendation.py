#!/usr/bin/python
import numpy as np
import heapq
import math
from math import sqrt

''' SETUP RATING MATRIX '''
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


''' COSINE FUNCTIONS '''
#  return cosine similarity between two vectors
def calculate_cosine_similarity(v1, v2, ratings):
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

def weighted_average(movie, neighbors, ratings, at_user):
    if 299 < at_user < 400:
        at_user -= 100
    elif 399 < at_user < 500:
        at_user -= 200

    sum = 0
    count = 0
    for neighbor in neighbors:
        score = map(float, ratings[neighbor][movie])[0]
        if score > 0:
            cos_sim = calculate_cosine_similarity(ratings[at_user], ratings[neighbor], ratings)
            sum += score * cos_sim
            count += cos_sim
    print count
    if count == 0:
        print "NOOOOOOO"
        return 4
    avg = sum / count
    return int(round(avg))
    # return avg


''' PEARSON FUNCTIONS '''
def average(x):
    assert len(x) > 0
    sum = 0
    for element in x:
        sum += int(element)
    return float(sum) / len(x)


def get_ni():
    ni_list = []
    for i in range(len(ratings[0])):
        ni_list.append(0)
    ni = 0
    for user in range(len(ratings)):
        for movie in range(len(ratings[user])):
            if ratings[user][movie] != '0':
                ni_list[movie] += 1
    return ni_list


def calculate_pearson_similarity(x, y, ratings):
    # x = [1]
    # y = [2]
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0

    for idx in range(n):
        n = len(ratings)
        ni = ni_list[idx]
        # print n
        # print ni
        if ni == 0:
            iuf = math.log(300)
        else:
            iuf = math.log(n / ni)
        f2 = iuf * iuf  # IUF

        xdiff = float(x[idx]) - avg_x
        ydiff = float(y[idx]) - avg_y
        diffprod += f2 * xdiff * ydiff
        xdiff2 += f2 * xdiff * xdiff
        ydiff2 += f2 * ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)


def pearson_prediction(movie, neighbors, ratings, at_user):
    if 299 < at_user < 400:
        at_user -= 100
    elif 399 < at_user < 500:
        at_user -= 200

    aSum = []
    for rating in ratings[at_user]:
        # rating = float(rating)
        if rating != '0':
            aSum.append(rating)
    ra = average(aSum)

    sumNum = 0
    sumDen = 0
    # print neighbors

    for neighbor in neighbors:
        if ratings[neighbor][movie] != '0':

            wau = calculate_pearson_similarity(ratings[at_user], ratings[neighbor], ratings)
            wau = wau * pow(abs(wau), 2.5)

            uSum = []
            for rn in ratings[neighbor]:
                if rn != '0':
                    uSum.append(rn)
            ru = average(uSum)

            rui = float(ratings[neighbor][movie])
            num = wau * (rui - ru)
            sumNum += num
            den = abs(wau)
            sumDen += den
    weight = 0
    if sumDen != 0:
        weight = sumNum/sumDen
    pai = ra + weight

    if pai > 5:
        pai = 5
    if pai < 1:
        pai = 1
    return int(round(pai))


''' USER BASED (COSINE AND PEARSON) FUNCTION '''
#  return indexes of the nearest n neighbors based on given similarity algorithm
def get_neighbors(n, index, ratings, return_positives, similarity):
    if 299 < index < 400:
        index -= 100
    elif 399 < index < 500:
        index -= 200

    sim_list = []
    i = 0
    for r1 in ratings:
    # for r1 in range(0, len(ratings)):

        if i != index:
            sim = similarity(r1, ratings[index], ratings)
            # print index, ", ", i, ', ', sim
            # print ratings[index]
            # print r1
            sim_list.append(sim)
        i += 1

    indexes = sorted(range(len(sim_list)), key=lambda x: sim_list[x])[-n:]
    if return_positives:  # return greatest positive values or greatest negative values
        indexes.reverse()
    for ind in range(0, len(indexes)): # fix user >200 index off by 1 error
        if indexes[ind] >= 200:
            indexes[ind] += 1
    print index
    print indexes
    print "cos sims: ", heapq.nlargest(n, (s for s in sim_list))
    # print "cos sims: ", heapq.nsmallest(n, (s for s in sim_list))

    #   print out how many movies rated that users have in common
    # for i in indexes:
    #     common = 0
    #     print 'index: ', i
    #     for s in range(0, len(ratings[i])):
    #         if ratings[i][s] != '0' and ratings[index][s] != '0':
    #             # print ratings[i][s]
    #             # print ratings[index][s]
    #             common += 1
    #     print 'common: ', common
    return indexes


''' ITEM BASED FUNCTIONS '''
def avg_rating(x):
    assert len(x) > 0
    sum = 0
    count = 0
    for element in x:
        if int(element) > 0:
            sum += int(element)
            count += 1
    return float(sum) / count

def calculate_item_similarity(x, y):
    sum_num = 0
    sum_den1 = 0
    sum_den2 = 0
    for u in range(300):
        ru = avg_usr_rating[u]
        rui = float(x[u])
        ruj = float(y[u])
        if rui != 0 and ruj != 0 and rui != ruj:
            sum_num += (rui - ru) * (ruj - ru)
            sum_den1 += (rui - ru) * (rui - ru)
            sum_den2 += (ruj - ru) * (ruj - ru)
    den = sqrt(sum_den1) * sqrt(sum_den2)
    if den == 0:
        # print 'den = 0'
        return 0.01
    sim = abs(sum_num / den)
    if sim == 1:
        # print 'sim == 1'
        return 0.02
    else:
        return sim

def item_prediction(movie, at_user):
    if 299 < at_user < 400:
        at_user -= 100
    elif 399 < at_user < 500:
        at_user -= 200

    sum_num = 0
    sum_den = 0
    for j in range(len(ratings[at_user])):
        if ratings[at_user][j] != '0':
            # j = int(j)
            wij = float(item_matrix[movie][j])
            # print 'wij: ', wij
            # print at_user, j
            raj = int(ratings[at_user][j])
            # raj = avg_rating(trans[j])
            # print raj
            sum_num += wij * raj
            sum_den += wij
    if sum_den != 0:
        pai = sum_num / sum_den
    else:
        pai = avg_usr_rating[at_user]
    return int(round(pai))


''' GENERAL ALGORITHM RESULT FILE '''
# parse input file and generate ratings for each 0 rating
def write_result(ratings, inFile, outFile, algorithm):
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
                if algorithm == 'cosine':
                    neighbors = get_neighbors(20, user, ratings, True, similarity=calculate_cosine_similarity)
                elif algorithm == 'pearson':
                    neighbors = get_neighbors(20, user, ratings, True, similarity=calculate_pearson_similarity)
                # elif algorithm == 'item':
                #     neighbors = get_item_neighbors(20, user)
                at_user = user;
            if algorithm == 'cosine':
                rows[i][2] = str(weighted_average(movie, neighbors, ratings, at_user))
            elif algorithm == 'pearson':
                rows[i][2] = str(pearson_prediction(movie, neighbors, ratings, at_user))
            elif algorithm == 'item':
                # rows[i][2] = str(item_prediction(movie, neighbors, ratings, at_user))
                rows[i][2] = str(item_prediction(movie, at_user))
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

# def calculate_item_similarity(x, y, trans):
#     for i in range(x):


avg_usr_rating = []
for user in ratings:
    avg_usr_rating.append(avg_rating(user))

item_matrix = []
try:
    f = open('item_matrix.txt', 'r')
    item_matrix = [map(str, line.split(',')) for line in f]
    trans = zip(*ratings)

except IOError:
    print 'initializing item matrix...'
    trans = zip(*ratings)
    for i in range(1000):
        item_matrix.append([0] * 1000)
        for j in range(1000):
            item_matrix[i][j] = calculate_item_similarity(trans[i], trans[j])
            # item_matrix[i][j] = 1
            print "calculate_item_similarity: ", i, j

    f = open('item_matrix.txt', 'w')
    for row in item_matrix:
        for column in row:
            line = str(column) + ','
            f.write(line)
        f.write('\n')
    f.close()


# write_result(ratings, inFile, outFile, 'cosine');
# ni_list = get_ni() # for pearson
# write_result(ratings, inFile, outFile, 'pearson');
write_result(ratings, inFile, outFile, 'item');


















# WEIGHTED AVERAGE ISNT WEIGHTED! CURRENTLY USING SIMPLE AVERAGE
#   AH BUT EVERYTHING IS BASICALLY .99 COSINE SIM ALREADY
# LOG SCALE HIGHER DIMENSION NEIGHBORS HIGHER * * *
# ADDRESS NOOOOOO?
# FILTER USERS WITH THAT MOVIE FIRST, THEN FIND NEIGHBORS?
#   BUT THAT WOULD MEAN YOU HAVE TO CALCULATE NEIGHBORS FOR EACH MOVIE
# Smooth the average for a user who rates fewer movies, using the general average for that movie

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
