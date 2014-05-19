#!/usr/bin/env python
#-*-coding:utf8-*-
'''
Created on 2013-10-14
@author: zyy_max
@brief: launch entry of near-duplicate detection system
'''

import os
import sys
from tokens import JiebaTokenizer
from simhash_imp import SimhashBuilder, hamming_distance
from features import FeatureBuilder

if __name__=="__main__":
    if len(sys.argv) < 7:
        print "Usage:\tlaunch.py word_dict_path stop_words_path fingerprint_path documents_path test_path result_path"
        exit(-1)
    # Load word list
    word_list = []
    with open(sys.argv[1], 'r') as ins:
        for line in ins.readlines():
            word_list.append(line.split()[1])
    # Init tokenizer
    jt = JiebaTokenizer(sys.argv[2], 'c')
    # Init feature_builder
    word_dict = {}
    for idx, ascword in enumerate(word_list):
        word_dict[ascword.decode('utf8')] = idx
    fb = FeatureBuilder(word_dict)
    # Init simhash_builder
    smb = SimhashBuilder(word_list)
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
            if lineidx != 642:
                continue
            # Tokenize
            tokens = jt.tokens(line.strip().decode('utf8'))
            # Compute text feature
            feature = fb.compute(tokens)
            # Compute simhash
            fingerprint = smb.sim_hash(feature)
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
    print min_sim, min_docid

