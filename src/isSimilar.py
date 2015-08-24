#!/usr/bin/env python
# -*-coding:utf8-*-
'''
Created on 2013-11-06
@author zyy_max
@brief check the similarity of 2 documents by VSM+cosine distance or simhash+hamming distance
'''
import sys
from simhash_imp import SimhashBuilder, hamming_distance
from tokens import JiebaTokenizer
from features import FeatureBuilder
from Utils import norm_vector_nonzero, cosine_distance_nonzero


class DocFeatLoader:
    def __init__(self, simhash_builder, feat_nonzero):
        self.feat_vec = feat_nonzero
        self.feat_vec = norm_vector_nonzero(self.feat_vec)
        self.fingerprint = simhash_builder.sim_hash_nonzero(self.feat_vec)


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print "Usage:\tisSimilar.py <doc1> <doc2> <stopword_path> <word_dict> <-c/-s> <threshold>"
        exit(-1)
    doc_path_1, doc_path_2, stopword_path, word_dict, mode, threshold = sys.argv[1:]
    print 'Arguments:', sys.argv[1:]
    with open(doc_path_1) as ins:
        doc_data_1 = ins.read().decode('utf8')
        print 'Loaded', doc_path_1
    with open(doc_path_2) as ins:
        doc_data_2 = ins.read().decode('utf8')
        print 'Loaded', doc_path_2

    # Init tokenizer
    jt = JiebaTokenizer(stopword_path, 'c')

    # Tokenization
    doc_token_1 = jt.tokens(doc_data_1)
    doc_token_2 = jt.tokens(doc_data_2)

    print 'Loading word dict...'
    # Load word list from word_dict
    word_list = []
    with open(word_dict, 'r') as ins:
        for line in ins.readlines():
            word_list.append(line.split()[1])

    # Build unicode string word dict
    word_dict = {}
    for idx, ascword in enumerate(word_list):
        word_dict[ascword.decode('utf8')] = idx
        # Build nonzero-feature
    fb = FeatureBuilder(word_dict)
    doc_feat_1 = fb.compute(doc_token_1)
    doc_feat_2 = fb.compute(doc_token_2)

    # Init simhash_builder
    smb = SimhashBuilder(word_list)

    doc_fl_1 = DocFeatLoader(smb, doc_feat_1)
    doc_fl_2 = DocFeatLoader(smb, doc_feat_2)

    if mode == '-c':
        print 'Matching by VSM + cosine distance'
        dist = cosine_distance_nonzero(doc_fl_1.feat_vec, doc_fl_2.feat_vec, norm=False)
        if dist > float(threshold):
            print 'Matching Result:\t<True:%s>' % dist
        else:
            print 'Matching Result:\t<False:%s>' % dist
    elif mode == '-s':
        print 'Matching by Simhash + hamming distance'
        dist = hamming_distance(doc_fl_1.fingerprint, doc_fl_2.fingerprint)
        if dist < float(threshold):
            print 'Matching Result:\t<True:%s>' % dist
        else:
            print 'Matching Result:\t<False:%s>' % dist
