#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 20150825
@author:    zyy_max

@brief: unit test of src/tokens.py
'''
import unittest
import sys
sys.path.append('..')
from src.tokens import JiebaTokenizer


class JiebaTokenizerTestCase(unittest.TestCase):

    def setUp(self):
        self.jt = JiebaTokenizer("../data/stopwords.txt")

    def testTokens(self):
        in_text = u"完整的单元测试很少只执行一个测试用例，" \
                  u"开发人员通常都需要编写多个测试用例才能" \
                  u"对某一软件功能进行比较完整的测试，这些" \
                  u"相关的测试用例称为一个测试用例集，在" \
                  u"PyUnit中是用TestSuite类来表示的。"
        tokens_text = u"完整/单元/测试/单元测试/只/执行/" \
                      u"一个/测试/试用/测试用例/开发/发人/" \
                      u"人员/开发人员/通常/需要/编写/多个/" \
                      u"测试/试用/测试用例/软件/功能/进行/" \
                      u"比较/完整/测试/相关/测试/试用/测试用例/" \
                      u"称为/一个/测试/试用/测试用例/集/PyUnit/" \
                      u"中是/TestSuite/类来/表示"
        self.assertEqual(tokens_text, u'/'.join(self.jt.tokens(in_text)), "Tokenization Results differ")

if __name__ == "__main__":
    unittest.main()
