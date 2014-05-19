#!/usr/bin/env python
'''
Created on 2013-11-14
@author zyy_max
@brief DocDict for loading docs from db or file, update and save them
'''

class DocDict(dict):
    """
    @brief load docs, update and 
    """
    def __init__(self, fpath=None):
        self.fpath = fpath
        if fpath is not None:
            self.load_from_file(fpath)
    def load_from_db(self):
        print 'Loading from db' 
        self.clear()
    def load_from_file(self, fpath):
        print 'Loading documents from file:',fpath
        self.fpath = fpath
        self.clear()
        with open(fpath, 'r') as ins:
            for line in ins.readlines():
                docid, doc_str = line.strip().split('\t')
                self[int(docid)] = doc_str
        return self
    def update(self, docid, doc_str):
        if not docid in self:
            self[docid] = doc_str
        return self
    def save_to_file(self, fpath):
        with open(fpath, 'w') as outs:
            for key in sorted(self.keys()):
                outs.write('%s\t%s\n' %(key, self[key]))
    def __del__(self):
        self.save_to_file(self.fpath)


