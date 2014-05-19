#!/usr/bin/env python
#-*-coding:utf8-*-
'''
@Created on 2013-10-21
@author zyy_max
@brief utils of common methods
@modified on 2013-10-23 ==> change break condition of cosine(euclidean)_distance_nonzero
'''

import math

def norm_vector_nonzero(ori_vec):
    ori_sum = math.sqrt(sum([math.pow(float(value),2) for (idx,value) in ori_vec]))
    if ori_sum < 1e-6:
        return ori_vec
    result_vec = []
    for idx, ori_value in ori_vec:
        result_vec.append((idx, float(ori_value)/ori_sum))
    #print ori_sum
    return result_vec

def cosine_distance_nonzero(feat_vec1, feat_vec2, norm=True):
    if True == norm:
        feat_vec1 = norm_vector_nonzero(feat_vec1)
        feat_vec2 = norm_vector_nonzero(feat_vec2)
    dist = 0
    idx1 = 0
    idx2 = 0
    while idx1 < len(feat_vec1) and idx2 < len(feat_vec2):
        if feat_vec1[idx1][0] == feat_vec2[idx2][0]:
            dist += float(feat_vec1[idx1][1])*float(feat_vec2[idx2][1])
            idx1 += 1
            idx2 += 1
        elif feat_vec1[idx1][0] > feat_vec2[idx2][0]:
            idx2 += 1
        else:
            idx1 += 1
    return dist

def euclidean_distance_nonzero(feat_vec1, feat_vec2, norm=True):
    if True == norm:
        feat_vec1 = norm_vector_nonzero(feat_vec1)
        feat_vec2 = norm_vector_nonzero(feat_vec2)
    dist = 0
    length = min(len(feat_vec1), len(feat_vec2))
    idx1 = 0
    idx2 = 0
    while idx1 < len(feat_vec1) and idx2 < len(feat_vec2):
        if feat_vec1[idx1][0] > feat_vec2[idx2][0]:
            dist += math.pow(float(feat_vec2[idx2][1]), 2)
            idx2 += 1
        elif feat_vec1[idx1][0] < feat_vec2[idx2][0]:
            dist += math.pow(float(feat_vec1[idx1][1]), 2)
            idx1 += 1
        else:
            dist += math.pow(float(feat_vec1[idx1][1])-float(feat_vec2[idx2][1]), 2)
            idx2 += 1
            idx1 += 1
    return math.sqrt(dist)

def norm_vector(ori_vec):
    ori_sum = math.sqrt(sum([math.pow(float(x),2) for x in ori_vec]))
    if ori_sum < 1e-6:
        return ori_vec
    result_vec = []
    for ori_value in ori_vec:
        result_vec.append(float(ori_value)/ori_sum)
    #print ori_sum
    return result_vec

def cosine_distance(feat_vec1, feat_vec2, norm=True):
    dist = 0
    if True == norm:
        feat_vec1 = norm_vector(feat_vec1)
        feat_vec2 = norm_vector(feat_vec2)
    for idx, feat1 in enumerate(feat_vec1):
        if idx >= len(feat_vec2):
            break
        if abs(float(feat1)) < 1e-6  or abs(float(feat_vec2[idx])) < 1e-6:
            continue
        dist += float(feat1)*float(feat_vec2[idx])
        #print dist
    return dist

def euclidean_distance(feat_vec1, feat_vec2, norm=True):
    dist = 0
    if True == norm:
        feat_vec1 = norm_vector(feat_vec1)
        feat_vec2 = norm_vector(feat_vec2)
    len1 = len(feat_vec1)
    len2 = len(feat_vec2)
    for idx in xrange(min(len2,len2)):
        dist += math.pow(float(feat_vec1[idx])-float(feat_vec2[idx]),2)
    if len1 < len2:
        dist += sum([math.pow(float(feat),2) for feat in feat_vec2[len1-len2:]])
    if len1 > len2:
        dist += sum([math.pow(float(feat),2) for feat in feat_vec1[len2-len1:]])
    return math.sqrt(dist)


