#!/usr/bin/env python
'''
Created on 2013-11-14
@author zyy_max
@brief utils for word dictionary
'''

class WordDict(dict):
    """
    @brief init, update and save word dictionary
    """
    def __init__(self, dict_path=None):
        if dict_path is not None:
            self.load_dict(dict_path)
    def load_dict(self, dict_path):
        self.dict_path = dict_path
        print 'Loading word dictionary from %s...' % dict_path
        self.clear()
        with open(dict_path, 'r') as ins:
            for line in ins.readlines():
                wordid, word = line.strip().split()
                if isinstance(word, str):
                    word = word.decode('utf8')
                self[word] = int(wordid)
        return self
    def add_one(self, word):
        if isinstance(word, str):
            word = word.decode('utf8')
        if not word in self:
            max_id = max([0] + self.values())
            self[word] = max_id+1
        return self
    def save_dict(self, dict_path):
        print 'Saving word dictionary to %s...' % dict_path
        word_list = self.items()
        with open(dict_path, 'w') as outs:
            for word, wordid in sorted(word_list):
                outs.write('%s\t%s\n' % (wordid, word)) 
    def __del__(self):
        self.save_dict(self.dict_path)
       
