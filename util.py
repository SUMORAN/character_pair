# -*- encoding: utf-8 -*-
import gensim.models
from gensim.models import word2vec
import tensorflow as tf
# import numpy as np
import codecs, sys
import json
import re


RAW_TEXT_PATH = "extracted_news.txt" # 未分词中文语料
PARTED_TEXT_PATH = "parted_text.txt" # 分词后中文语料
WORD2VEC_TRAIN_FILE = "parted_text.txt"
WORD2VEC_MODEL_PATH = "word2vec.model"  # 词向量模型路径
word_vector_path = "word2vec_d100.vector"  # 词向量文件路径
# TEXT_LABEL_PATH = "yelp_data/yelp_5000"  # 带标注的文本文件路路径
# Embedding_Dimention = 100



def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    This is for splitting English, changing all word to lowercase.
    """
    # 清理数据替换掉无词义的符号
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

# 移除每行文本中的无用词语和标点
def rm_useless_tokens(line):
    new_line = line.replace('.', '').replace('（', '').replace('）', '')\
        .replace('？', ' ').replace('！', ' ').replace('-', '').replace('/', '').replace('，', '').replace('@', '')\
        .replace("\"", " ").replace("：", " ").replace('=', '').replace('【', '').replace('】', '').replace('+', '')\
        .replace('；', '').replace('*', '').replace('_', '').replace('\'s', '').replace('\' ', '').replace('\n', '')\
        .replace('~', '').replace('', '').replace('。', '').replace('、', '').replace('|', '').replace('１', '9')\
        .replace('２', '9').replace('３', '9').replace('４', '9').replace('５', '9').replace('６', '9').replace('７', '9') \
        .replace('８', '9').replace('９', '9').replace('．', '9').replace('／', '')
    return new_line.strip().lower()


# 分词
def ChineseParticiple(raw_text_path=RAW_TEXT_PATH, parted_text_path=PARTED_TEXT_PATH):
    print('\033[1;33mStart participate Chinese\033[0m')
    f = codecs.open(raw_text_path, 'r', encoding='utf-8')
    target = codecs.open(parted_text_path, 'w', encoding='utf-8')

    lineNum = 0
    for line in f.readlines():
        lineNum = lineNum + 1
        print('---------processing', lineNum, 'article---------')
        # seg_list = jieba.cut(line, cut_all=False)
        # line = clean_str(line)
        line = rm_useless_tokens(line).strip()
        line = line.replace('的跳', '的 跳')
        seg_list = []
        for x in line:
            if x != ' ':
                seg_list.append(x)
        # seg_list.append('\n')
        line_seg = '\n'.join(seg_list)
        target.writelines(line_seg)

    print('\033[1;33mparticipate Chinese DONE!\033[0m')
    f.close()
    target.close()

# 训练词向量模型，并将模型对应词向量字典保存至文件
def train_word2vec(train_file_path = WORD2VEC_TRAIN_FILE):
    sentences = word2vec.Text8Corpus(train_file_path)
    # model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    # model.train(more_sentences)
    model = word2vec.Word2Vec(sentences, sg=1, min_count=5, window=5, size=100) # sg = 1：skip-gram   size:dimention

    # 保存词向量模型
    model.save(WORD2VEC_MODEL_PATH)
    # # 将模型对应词向量字典保存至文件
    model.wv.save_word2vec_format(word_vector_path, binary=False)

    # # 将模型对应词向量字典保存至文件
    # tokenizer = tf.keras.preprocessing.text.Tokenizer()  # 参数num_words: 需要保留的最大词数，基于词频。只有最常出现的 num_words 词会被保留。
    # tokenizer.fit_on_texts(sentences)
    # vocab_size = len(tokenizer.word_index) + 1
    # print('vocab_size = {}'.format(vocab_size))
    # embedding_dict = {}
    # for word, i in tokenizer.word_index.items():
    #     try:
    #         embedding_vec = model[word]
    #         embedding_dict[word] = embedding_vec
    #     except KeyError:
    #         continue
    # # js = json.dumps(embedding_dict)
    # # file = open('word_vector_path', 'w')
    # # file.write(js)
    # # file.close()
    # # print('word2vec dictionary has been saved!')
    # #
    # # # 读取字典
    # # # import json
    # # # file = open('word_vector_path', 'r')
    # # # js = file.read()
    # # # dic = json.loads(js)
    # # # print(dic)
    # # # file.close()
    # # 这里存下的文件需要手动加入文件第一行 vocab_size dimention
    # fw = open("word_vector_path", 'w+')
    # fw.write(str(embedding_dict))  # 把字典转化为str
    # fw.close()

#     # 读取字典
#     # fr = open("word_vector_path", 'r+')
#     # dic = eval(fr.read())  # 读取的str转换为字典
#     # print(dic)
#     # fr.close()

#     # 测试词向量模型
#     print("Finish training. Word2vec Model saved!")
#     sim_word = model.most_similar(["several"], topn=5)
#     for word in sim_word:
#         for w in word:
#             print(w)


# # 基于预训练词向量模型将句子的单词序列转换为向量序列，返回句子的矩阵和类别标记
# def generate_sentence_matrix_form_word2vec_model():
#     model = gensim.models.Word2Vec.load(WORD2VEC_MODEL_PATH)  # 载入word2vec模型
#     text_file = open(TEXT_LABEL_PATH, 'r', encoding='UTF-8')
#     labels = []  # 句子类别列表
#     sentences = []
#     for line in text_file.readlines():
#         # 将句子和标签分别单独摘出来
#         if ' 5\n' in line:
#             labels.append(5)
#         elif ' 1\n' in line:
#             labels.append(1)
#         elif ' 2\n' in line:
#             labels.append(2)
#         elif ' 3\n' in line:
#             labels.append(3)
#         elif ' 4\n' in line:
#             labels.append(4)
#         elif ' 0\n' in line:
#             labels.append(0)
#         else:
#             labels.append(999)

#         sentence = line.replace(' 1\n', '').replace(' 0\n', '').replace(' 2\n', '').replace(' 3\n', '')\
#             .replace(' 4\n', '').replace(' 5\n', '')
#         for word in sentence:
#             try:
#                 sentence.replace(word, str(model[word]))
#             except KeyError:
#                 # 以下这种方法不太合理，会使得同一个单词在不同句子中的向量表示不一样
#                 sentence.replace(word, str(np.random.uniform(-0.25, 0.25, 100))) # 100维

#         sentences.append(sentence)
#     text_file.close()

#     padded_sentences = tf.keras.preprocessing.sequence.pad_sequences(sentences, maxlen=10, padding='post') # 填充序列

#     return padded_sentences, labels

# # 基于预训练词向量文件（例如glove）将句子的单词序列转换为向量序列，返回句子的矩阵和类别标记
# def generate_sentence_matrix_form_word2vec_file():
#     # 读取字典
#     fr = open("word_vector_path", 'r+')
#     word2vec_dic = eval(fr.read())  # 读取的str转换为字典
#     # print(word2vec_dic)
#     fr.close()
#     text_file = open(TEXT_LABEL_PATH, 'r', encoding='UTF-8')
#     labels = []  # 句子类别列表
#     sentences = []
#     for line in text_file.readlines():
#         # 将句子和标签分别单独摘出来
#         if ' 5\n' in line:
#             labels.append(5)
#         elif ' 1\n' in line:
#             labels.append(1)
#         elif ' 2\n' in line:
#             labels.append(2)
#         elif ' 3\n' in line:
#             labels.append(3)
#         elif ' 4\n' in line:
#             labels.append(4)
#         elif ' 0\n' in line:
#             labels.append(0)
#         else:
#             labels.append(999)

#         sentence = line.replace(' 1\n', '').replace(' 0\n', '').replace(' 2\n', '').replace(' 3\n', '')\
#             .replace(' 4\n', '').replace(' 5\n', '')
#         for word in sentence:
#             try:
#                 sentence.replace(word, str(word2vec_dic[word]))
#             except KeyError:
#                 word2vec_dic[word] = np.random.uniform(-0.25, 0.25, 100) # 100维
#                 sentence.replace(word, str(word2vec_dic[word]))
#         sentences.append(sentence)
#     text_file.close()

#     padded_sentences = tf.keras.preprocessing.sequence.pad_sequences(sentences, maxlen=10, padding='post')  # 填充序列

#     return padded_sentences, labels



if __name__ == "__main__":
    
    ChineseParticiple('extracted_news.txt', 'parted_text_lines.txt')
    print("word2vec model has created!")
    # train_word2vec()
    # generate_sentence_matrix_form_word2vec_model()
    # generate_sentence_matrix_form_word2vec_file()
    print("word2vec model has created!")
    #





