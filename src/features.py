#!/usr/bin/python
#-*-coding:utf8-*-
'''
Created on 2013-10-13
@author: zyy_max
@brief: build feature vector with word_dict and token_list
@modified: 2013-10-15 ==> add upate_word for FeatureBuilder
@modified: 2013-11-06 ==> add feature_nonzero
@modified: 2013-11-15 ==> add FeatureBuilderUpdate
                          word_dict is WordDict in DictUtils
'''
import os,sys
class FeatureBuilder:
    def __init__(self, word_dict):
        self.word_dict = word_dict
    
    def compute(self, token_list):
        feature = [0]*len(self.word_dict)
        for token in token_list:
            feature[self.word_dict[token]] += 1
        feature_nonzero = [(idx,value) for idx, value in enumerate(feature) if value > 0]
        return feature_nonzero

    def _add_word(self, word):
        if not word in self.word_dict:
            self.word_dict[word] = len(self.word_dict)

    def update_words(self, word_list=[]):
        for word in word_list:
            self._add_word(word)

class FeatureBuilderUpdate(FeatureBuilder):
    def _add_word(self, word):
        self.word_dict.add_one(word)


def feature_single(inputfile, outputfile):
    print inputfile,outputfile
    result_lines = []
    with open(inputfile, 'r') as ins:
        for lineidx, line in enumerate(ins.readlines()):
            feature = fb.compute([token.decode('utf8') for token in line.strip().split()])
            l = []
            for idx,f in feature:
                if f > 1e-6:
                    l.append('%s:%s' %(idx,f))
            result_lines.append(' '.join(l) + os.linesep)
            print 'Finished\r', lineidx,
    with open(outputfile, 'w') as outs:
        outs.writelines(result_lines)
    print 'Wrote to ', outputfile

if __name__=="__main__":
    if len(sys.argv) < 5:
        print "Usage:\tfeature.py -s/-m <word_dict_path> <tokens_file/tokens_folder> <feature_file/feature_folder>"
        exit(-1)
    word_dict = {}
    with open(sys.argv[2], 'r') as ins:
        for line in ins.readlines():
            l = line.split()
            word_dict[l[1].decode('utf8')] = int(l[0])
    fb = FeatureBuilder(word_dict)
    print 'Loaded', len(word_dict), 'words'
    if sys.argv[1] == '-s':
        feature_single(sys.argv[3], sys.argv[4])
    elif sys.argv[1] == '-m':
        for inputfile in os.listdir(sys.argv[3]):
            feature_single(os.path.join(sys.argv[3],inputfile), os.path.join(sys.argv[4],inputfile.replace('.token','.feat')))
