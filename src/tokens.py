#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 20131012
@author:    zyy_max

@brief: get tokens from input file by jieba
'''
import jieba
import os
import sys


class JiebaTokenizer:
    def __init__(self, stop_words_path, mode='s'):
        self.stopword_set = set()
        # load stopwords
        with open(stop_words_path) as ins:
            for line in ins:
                self.stopword_set.add(line.strip().decode('utf8'))
        self.mode = mode

    def tokens(self, intext):
        intext = u' '.join(intext.split())
        if self.mode == 's':
            token_list = jieba.cut_for_search(intext)
        else:
            token_list = jieba.cut(intext)
        return [token for token in token_list if token.strip() != u'' and not token in self.stopword_set]


def token_single_file(input_fname, output_fname):
    result_lines = []
    with open(input_fname) as ins:
        for line in ins:
            line = line.strip().decode('utf8')
            tokens = jt.tokens(line)
            result_lines.append(u' '.join(tokens).encode('utf8'))
    open(output_fname, 'w').write(os.linesep.join(result_lines))
    print 'Wrote to ', output_fname


if __name__ == "__main__":
    if len(sys.argv) < 6 or sys.argv[1] not in ['-s', '-m'] or sys.argv[4] not in ['c', 's']:
        print "Usage:\ttokens.py <file_mode(-s/-m)> <input_file/input_folder> " \
              "<output_file/output_folder> <cut_mode(c/s)> <stopword.list>"
        print "file_mode:\t-s:\tsingle file"
        print "\t\t-m:\tmultiple files"
        print "cut_mode:\tc:\tnormal mode of Jieba"
        print "\t\ts:\tcut_for_search mode of Jieba"
        exit(-1)
    file_mode, input_filepath, output_filepath, cut_mode, stopword_file = sys.argv[1:]
    jt = JiebaTokenizer(stopword_file, cut_mode)
    # extract tokens and filter by stopwords
    if file_mode == '-s':
        token_single_file(input_filepath, output_filepath)
    elif file_mode == '-m':
        for input_file in os.listdir(input_filepath):
            prefix = input_file.rsplit(os.sep, 1)[0]
            token_single_file(os.path.join(input_filepath, input_file),
                              os.path.join(output_filepath, prefix+'.token'))
