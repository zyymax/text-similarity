text-similarity
===============
By max.zhang@2013-11-06

说明：本项目为python语言实现的文本相似度检测工具

# 环境依赖
*	python
*	python-jieba
*	bash

# 目录说明
data 文件夹

	-stopwords.txt （停用词表）

data/temp 文件夹 （存放中间结果文件和文件夹，文件中每一行均表示一个文档）

	-*.content	网页解析后的原始文本（有噪声）

	-*.ori		经过预处理后的，可用于检测的原始文本（去噪）

	-*.token		中文分词结果

	-word.dict	根据分词结果生成的特征词典

	-*.feat		特征向量文件

	-*.fprint		Simhash信息指纹文件

src/ 文件夹  

	源程序


# 代码使用说明

## 判断两个文档的重复度（整合）

### 生成特征词典 (preprocess.py)

brief: 对原始文本进行分词并将结果添加到特征词典中

INPUT: 原始文本 + 停用词表 + 特征词典

OUTPUT: 将分词结果保存到.token中，并更新特征词典文件

usage:

	src/preprocess.py <*.ori> <stopword_path> <word_dict>

e.g.

	src/preprocess.py data/temp/doc1.ori data/stopwords.txt data/word.dict

{Note: 需对待比较的两个文档分别运行一次, i.e. 两个文档的分词结果都应添加到特征词典中}


### 判断文档重复度 (isSimilar.py)

brief: 判断两个文档是否重复

INPUT: 文档1 + 文档2 + 停用词表 + 特征词典 + 模式选择 + 阈值

OUTPUT: 输出两篇文档是否重复及相似度

usage:

	src/isSimilar.py <doc1> <doc2> <stopword_path> <word_dict> <-c/-s> <threshold>

	-c/-s	选择采用VSM+CosineDistance或是Simhash+HammingDistance方法进行重复判断

e.g.

	src/isSimilar.py data/temp/doc1.ori data/temp/doc2.ori data/stopwords.txt data/word.dict -c 0.8


## 详细处理流程（单步）

### 去噪 (webcontent-filter.sh)

brief: 原始文本的初步去噪（去特殊符号、英文字母、数字 ...），消除连续空格以及删除空白行

INPUT: 待去噪文本 (.content)

OUTPUT: 去噪后的文本 (.ori)

usage:

	src/webcontent_filter.sh <*.content> <*.ori>
	
e.g.

	src/webcontent-filter.sh data/temp/all.content data/temp/all.ori
	

### 预处理

#### 中文分词(tokens.py)

brief: 采用Jieba分词器对去噪后的原始文本进行中文分词

INPUT: 去噪后的文本 (.ori)

OUTPUT: 中文分词结果 (.token)

usage:

	./tokens.py  -s/-m <*.ori/inputfolder> <*.token/outputfolder> c/s[mode] <stopword.list>

	-s[single]/-m[multiple]  对单个文本文件 (*.ori) 或对文本文件目录进行分词

		-s <*.ori> <*.token>

		-m <inputfolder> <outputfolder> {Note: 采用-m模式时，原始文本名最好以.ori结尾}

	c/s[mode]	Jieba分词器模式选择

		c模式	jieba.cut(...)

		s模式	jieba.cut_for_search()

e.g.

	src/tokens.py  -s  data/temp/all.ori data/temp/all.token c data/stopwords.txt 


#### 生成特征词典 (DictBuilder.py)

brief: 根据分词结果文件或目录，生成以词频降序排列的特征词典

INPUT: 中文分词结果 (.token)

OUTPUT:生成的特征词典，词典格式如下：ID + 特征词 + 词频

usage:

	src/DictBuilder.py <input_folder/*.token> <output_file>

e.g.

	src/DictBuilder.py data/temp/all.token data/temp/word.dict


#### 生成特征向量 (features.py)

brief: 根据分词结果和特征词典，生成特征向量文件

INPUT: 第一步处理中分词后的文本 + 第二步生成的特征词典

OUTPUT: 以行为单位生成各文档的特征向量：id1:nonzero-tf id2:nonzero-tf ...

usage:

	src/feature.py -s/-m <word_dict_path> <tokens_file/tokens_folder> <feature_file/feature_folder>

	-s[single]/-m[multiple]  对单个分词文件 (*.token) 或对分词文件目录生成特征向量
	
e.g.

	src/feature.py -s data/temp/word.dict data/temp/all.token data/temp/all.feat


#### 生成Simhash指纹 (simhash_imp.py)

brief: 根据分词结果和特征词典，生成信息指纹文件

INPUT: 特征词典 + 特征向量文件

OUTPUT: 信息指纹文件

usage:

	src/simhash_imp.py <word_dict_path> <*.feat> <*.fprint>

e.g.

	src/simhash_imp.py data/temp/word.dict data/temp/all.feat data/temp/all.fprint

## 单元测试

    cd test
    python test_token.py
