#!/usr/bin/env python
#-*-coding:utf8-*-
'''
Created on 2013-10-15
@author: zyy_max
@brief: incremental-version launch entry of near-duplicate detection system
'''

import os
import sys
from tokens import JiebaTokenizer
from simhash_imp import SimhashBuilder, hamming_distance
from features import FeatureBuilder


class FeatureContainer:
    def __init__(self, word_dict_path):
        # Load word list
        self.word_dict_path = word_dict_path
        self.word_list = []
        with open(word_dict_path, 'r') as ins:
            for line in ins.readlines():
                self.word_list.append(line.split()[1])
        self.word_dict = {}
        for idx, ascword in enumerate(self.word_list):
            self.word_dict[ascword.decode('utf8')] = idx
        self.fb = FeatureBuilder(self.word_dict)
        self.smb = SimhashBuilder(self.word_list)
        print 'Loaded ', len(self.word_list), 'words'

    def compute_feature(self, token_list):
        new_words = []
        for token in token_list:
            if not token in self.word_dict:
                new_words.append(token)
        if len(new_words) != 0:
            # Update word_list and word_dict
            self.fb.update_words(new_words)
            self.smb.update_words([word.encode('utf8') for word in new_words])
            self.word_dict = self.fb.word_dict
            self.word_list.extend([word.encode('utf8') for word in new_words])
        feature_vec = self.fb.compute(token_list)
        return feature_vec, self.smb.sim_hash(feature_vec)
'''
    def __del__(self):
        with open(self.word_dict_path, 'w') as outs:
            for idx, word in enumerate(self.word_list):
                outs.write('%s\t%s%s'%(idx, word, os.linesep))
'''
if __name__=="__main__":
    if len(sys.argv) < 7:
        print "Usage:\tlaunch_inc.py <word_dict_path> <stop_words_path> <fingerprint_path> <documents_path> <test_path> <result_path>"
        exit(-1)
    # Init tokenizer
    jt = JiebaTokenizer(sys.argv[2], 'c')
    # Init feature_builder and simhash_builder 
    fc = FeatureContainer(sys.argv[1])
    # Load fingerprint list
    fingerprint_list = []
    with open(sys.argv[3], 'r') as ins:
        for line in ins.readlines():
            fingerprint_list.append(int(line))
    # For exp: load document content
    doc_list = []
    with open(sys.argv[4], 'r') as ins:
        for line in ins.readlines():
            doc_list.append(line.strip())
    # Detection process begins
    min_sim = 64
    min_docid = 0
    with open(sys.argv[5], 'r') as ins:
        for lineidx, line in enumerate(ins.readlines()):
            # Tokenize
            tokens = jt.tokens(line.strip().decode('utf8'))
            feature, fingerprint = fc.compute_feature(tokens)
            result_list = []
            for idx, fp in enumerate(fingerprint_list):
                sim = hamming_distance(fingerprint, fp, 64)
                result_list.append((sim, idx))
            result_list = sorted(result_list, cmp=lambda x,y: cmp(x[0],y[0]))
            if result_list[0][0] < min_sim:
                min_sim, min_docid = result_list[0][0], lineidx
            #'''
            with open(sys.argv[6], 'w') as outs:
                outs.write(line.strip()+os.linesep)
                for sim, idx in result_list:
                    outs.write('%s\t%s%s' %(sim, doc_list[idx], os.linesep)) 
            #'''
            #if lineidx == 2:
            #    break   
    with open('word_dict_new.txt', 'w') as outs:
        for idx, word in enumerate(fc.word_list):
            outs.write('%s\t%s%s'%(idx, word, os.linesep))
            
