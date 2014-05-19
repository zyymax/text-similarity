#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-10-13
@author: zyy_max
@brief: build simhash and compute hamming_distance
@modified: 2013-10-15 ==> add update_word for SimhashBuilder
'''

# Implementation of Charikar simhashes in Python
# See: http://dsrg.mff.cuni.cz/~holub/sw/shash/#a1

import os, sys

def hamming_distance(hash_a, hash_b, hashbits=128):
    x = (hash_a ^ hash_b) & ((1 << hashbits) - 1)
    tot = 0
    while x:
        tot += 1
        x &= x-1
    return tot
class SimhashBuilder:
    def __init__(self, word_list=[], hashbits=128):
        self.hashbits = hashbits
        self.hashval_list = [self._string_hash(word) for word in word_list]
        print 'Totally: %s words' %(len(self.hashval_list),)
        """
        with open('word_hash.txt', 'w') as outs:
            for word in word_list:
                outs.write(word+'\t'+str(self._string_hash(word))+os.linesep)
        """

    def _string_hash(self, word):
        # A variable-length version of Python's builtin hash
        if word == "":
            return 0
        else:
            x = ord(word[0])<<7
            m = 1000003
            mask = 2**self.hashbits-1
            for c in word:
                x = ((x*m)^ord(c)) & mask
            x ^= len(word)
            if x == -1:
                x = -2
            return x

    def sim_hash_nonzero(self, feature_vec):
        finger_vec = [0]*self.hashbits
        # Feature_vec is like [(idx,nonzero-value),(idx,nonzero-value)...]
        for idx, feature in feature_vec:
            hashval = self.hashval_list[int(idx)]
            for i in range(self.hashbits):
                bitmask = 1<<i
                if bitmask&hashval != 0:
                    finger_vec[i] += float(feature)
                else:
                    finger_vec[i] -= float(feature)
        #print finger_vec
        fingerprint = 0
        for i in range(self.hashbits):
            if finger_vec[i] >= 0:
                fingerprint += 1 << i
#整个文档的fingerprint为最终各个位大于等于0的位的和
        return fingerprint    
    
    def sim_hash(self, feature_vec):
        finger_vec = [0]*self.hashbits
        for idx, feature in enumerate(feature_vec):
            if float(feature) < 1e-6:
                continue
            hashval = self.hashval_list[idx]
            for i in range(self.hashbits):
                bitmask = 1<<i
                if bitmask&hashval != 0:
                    finger_vec[i] += float(feature)
                else:
                    finger_vec[i] -= float(feature)
        #print finger_vec
        fingerprint = 0
        for i in range(self.hashbits):
            if finger_vec[i] >= 0:
                fingerprint += 1 << i
#整个文档的fingerprint为最终各个位大于等于0的位的和
        return fingerprint

    def _add_word(self, word):
        self.hashval_list.append(self._string_hash(word))

    def update_words(self, word_list=[]):
        for word in word_list:
            self._add_word(word)

class simhash():
    def __init__(self, tokens='', hashbits=128):
        self.hashbits = hashbits
        self.hash = self.simhash(tokens)

    def __str__(self):
        return str(self.hash)

    def __long__(self):
        return long(self.hash)

    def __float__(self):
        return float(self.hash)

    def simhash(self, tokens):
        # Returns a Charikar simhash with appropriate bitlength
        v = [0]*self.hashbits

        for t in [self._string_hash(x) for x in tokens]:
            bitmask = 0
            #print (t)
            for i in range(self.hashbits):
                bitmask = 1 << i
                #print(t,bitmask, t & bitmask)
                if t & bitmask:
                    v[i] += 1 #查看当前bit位是否为1，是的话则将该位+1
                else:
                    v[i] += -1 #否则得话，该位减1

        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i
#整个文档的fingerprint为最终各个位大于等于0的位的和
        return fingerprint

    def _string_hash(self, v):
        # A variable-length version of Python's builtin hash
        if v == "":
            return 0
        else:
            x = ord(v[0])<<7
            m = 1000003
            mask = 2**self.hashbits-1
            for c in v:
                x = ((x*m)^ord(c)) & mask
            x ^= len(v)
            if x == -1:
                x = -2
            return x

    def hamming_distance(self, other_hash):
        x = (self.hash ^ other_hash.hash) & ((1 << self.hashbits) - 1)
        tot = 0
        while x:
            tot += 1
            x &= x-1
        return tot

    def similarity(self, other_hash):
        a = float(self.hash)
        b = float(other_hash)
        if a>b: return b/a
        return a/b

if __name__ == '__main__':
    #看看哪些东西google最看重？标点？
    #s = '看看哪些东西google最看重？标点？'
    #hash1 =simhash(s.split())
    #print("0x%x" % hash1)
    #print ("%s\t0x%x" % (s, hash1))

    #s = '看看哪些东西google最看重！标点！'
    #hash2 = simhash(s.split())
    #print ("%s\t[simhash = 0x%x]" % (s, hash2))

    #print '%f%% percent similarity on hash' %(100*(hash1.similarity(hash2)))
    #print hash1.hamming_distance(hash2),"bits differ out of", hash1.hashbits

    if len(sys.argv) < 4:
        print "Usage:\tsimhash_imp.py <word_dict_path> <feature_file> <finger_print_file>"
        exit(-1)
    word_list = []
    with open(sys.argv[1], 'r') as ins:
        for idx, line in enumerate(ins.readlines()):
            word_list.append(line.split()[1])
            print '\rloading word', idx,
    sim_b = SimhashBuilder(word_list)
    result_lines = []
    print ''
    with open(sys.argv[2], 'r') as ins:
        for idx, line in enumerate(ins.readlines()):
            print '\rprocessing doc', idx,
            feature_vec = line.strip().split()
            feature_vec = [(int(item.split(':')[0]),float(item.split(':')[1])) for item in feature_vec]
            fingerprint = sim_b.sim_hash_nonzero(feature_vec)
            result_lines.append(str(fingerprint)+os.linesep)
    with open(sys.argv[3], 'w') as outs:
        outs.writelines(result_lines)



