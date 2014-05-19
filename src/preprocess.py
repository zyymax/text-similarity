#!/usr/bin/env python
#-*-coding:utf8-*-
'''
Created on 2013-11-06
@author zyy_max
@brief update word_dict by token result of document
'''
import os
import sys
import time
from tokens import JiebaTokenizer
from DictBuilder import WordDictBuilder

if __name__=="__main__":
    if len(sys.argv) < 4:
        print "Usage:\tpreprocess.py <docpath> <stopword_path> <worddict_path>"
        exit(-1)
    doc_path, stopword_path, worddict_path = sys.argv[1:]
    print 'Arguments:',sys.argv[1:]
    
    # Init tokenizer
    jt = JiebaTokenizer(stopword_path, 'c')
    # Load doc data
    with open(doc_path) as ins:
        doc_data = ins.read().decode('utf8')
    # Tokenization
    doc_tokens = jt.tokens(doc_data)
    # Write to token file
    with open(doc_path[:doc_path.rfind('.')]+'.token', 'w') as outs:
        outs.write('/'.join([token.encode('utf8') for token in doc_tokens]))
    
    # Load original word dict, update and save
    wdb = WordDictBuilder(worddict_path, tokenlist=doc_tokens)
    wdb.run()
    wdb.save(worddict_path)
    print 'Totally', len(wdb.word_dict), 'words'
    
