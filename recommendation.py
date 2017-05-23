#!/usr/bin/python


def getRatings():
    i = 1;
    for line in open('train.txt'):
        print i, "\t", line;
        ratings = line.split('\t')[0:1000];
        print ratings;


        i+=1;

getRatings();