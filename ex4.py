# -*- encoding: utf-8 -*-
import math
import random
import codecs

RAW_TEXT_PATH = "zhangwenbin.txt" # 未分词中文语料
PARTED_TEXT_PATH = "parted_text.txt" # 分词后中文语料
WORD2IDX_PATH = 'word2idx_dic.txt'
IDX2WORD_PATH = 'idx2word_dic.txt'
TEST_PATH = 'test.txt'

# 移除每行文本中的无用词语和标点
def rm_useless_tokens(line):
    new_line = line.replace('.', '').replace('（', '').replace('）', '')\
        .replace('？', ' ').replace('！', ' ').replace('-', '').replace('/', '').replace('，', '').replace('@', '')\
        .replace("\"", " ").replace("：", " ").replace('=', '').replace('【', '').replace('】', '').replace('+', '')\
        .replace('；', '').replace('*', '').replace('_', '').replace('\'s', '').replace('\' ', '').replace('\n', '')\
        .replace('~', '').replace('', '').replace('。', '').replace('、', '').replace('|', '').replace('１', '9')\
        .replace('２', '9').replace('３', '9').replace('４', '9').replace('５', '9').replace('６', '9').replace('７', '9') \
        .replace('８', '9').replace('９', '9').replace('．', '9').replace('／', '').replace('“', '').replace('”', '')\
        .replace('‘', '').replace('’', '')
    return new_line.strip().lower()

'''
功能：分词
参数：
    raw_text_path：待分词文本文件
    parted_text_path：分词后文本文件
'''
def ChineseParticiple(raw_text_path=RAW_TEXT_PATH, parted_text_path=PARTED_TEXT_PATH):
    print('\033[1;33mStart participate Chinese\033[0m')
    f = codecs.open(raw_text_path, 'r', encoding='utf-8')
    target = codecs.open(parted_text_path, 'a', encoding='utf-8')

    # parted_text = []
    lineNum = 0
    for line in f.readlines():
        lineNum = lineNum + 1
        # print('---------processing', lineNum, 'article---------')
        # seg_list = jieba.cut(line, cut_all=False)
        # line = clean_str(line)
        # line = rm_useless_tokens(line).strip()
        seg_list = []
        for x in line:
            if x != ' ':
                seg_list.append(x)
                # parted_text.append(x)
        # seg_list.append('\n')
        line_seg = '\n'.join(seg_list)
        target.writelines(line_seg)
        

    print('\033[1;33mparticipate Chinese DONE!\033[0m')
    f.close()
    target.close()
    # return parted_text

    
'''
功能：从分词后文件生成字典
参数：
    parted_text_path：分词后文本文件
返回值：word_to_ix 和 ix_to_word（字典）
'''
def generate_dic(parted_text_path=PARTED_TEXT_PATH):
    f1 = open(parted_text_path, 'r', encoding='utf-8')
    print('Load raw text……')
    sentence = []
    # num = 0
    for line in f1.readlines():
        # num += 1
        # if num > 100000:
        #     break
        if line != '':  # 去除空白行
        # if line != '' and line != '9':  # 去除空白行
            sentence.append(line.strip())

    raw_text = sentence

    word_to_ix = {}
    ix_to_word = {}

    # 词汇表
    vocab = set(raw_text)
    vocab_size = len(vocab)

    # word to idx
    for i, word in enumerate(vocab):
        word_to_ix[word] = i

        ix_to_word[i] = word

    return word_to_ix, ix_to_word


'''
功能：将字典保存到本地
参数：
    dic: 待保存的字典
    dic_path：本地字典文件路径
'''
def save_dic(dic, dic_path):
    fw = open(dic_path, 'w+', encoding='utf-8')
    fw.write(str(dic))  # 把字典转化为str
    fw.close()


'''
功能：从本地读取字典
参数：
    dic_path：本地字典文件路径
返回值：字典
'''
def load_dic(dic_path):
    fr = open(dic_path, 'r+', encoding='utf-8')
    dic = eval(fr.read())  # 读取的str转换为字典
    fr.close()
    return dic


'''
功能：载入分词后文件
参数：
    parted_text_path：分词后文本文件
返回值：文本对应的list
'''
def load_rawText(parted_text_path=PARTED_TEXT_PATH):
    f1 = open(parted_text_path, 'r', encoding='utf-8')
    print('Load raw text……')
    sentence = []
    # num = 0
    for line in f1.readlines():
        # num += 1
        # if num > 100000:
        #     break
        if line != '':  # 去除空白行
        # if line != '' and line != '9':  # 去除空白行
            sentence.append(line.strip())

    return sentence


'''
功能：按照字典将文本替换为对应idx
参数：
    raw_text：待替换的文本list
    word_to_ix：word to idx字典
返回值：文本对应的数字表示list
'''
def word2idx(raw_text, word_to_ix):
    raw_text_idx = []
    for item in raw_text:
        if item in word_to_ix:
            item = item.replace(item, str(word_to_ix[item]))
        else:
            item = item.replace(item, str(random.randint(1, 2000)))
        raw_text_idx.append(item)
    return raw_text_idx


'''
功能：载入，进行judge之前应该先执行这个函数，并将返回值保存在变量中
参数：
    parted_text_path: 分词后文件路径
    word2idx_path： word to idx 字典路径
    idx2dic_path: idx 2 word 字典路径
返回值：raw_text, raw_text_idx, word2idx_dic, idx2word_dic
'''
def load(parted_text_path, word2idx_path, idx2dic_path):
    raw_text = load_rawText(parted_text_path)
    word2idx_dic = load_dic(word2idx_path)
    idx2word_dic = load_dic(idx2dic_path)
    raw_text_idx = word2idx(raw_text, word2idx_dic)

    context_list = []
    
    # window = 0
    for i in range(1, len(raw_text_idx) - 1):
        whole = [raw_text_idx[i]]
        context_list.append(whole)

    # window = 1
    for i in range(1, len(raw_text_idx) - 1):
        whole_left = [raw_text_idx[i - 1], raw_text_idx[i]]
        whole_right = [raw_text_idx[i], raw_text_idx[i + 1]]
        context_list.append(whole_left)
        context_list.append(whole_right)

    # window = 2
    for i in range(2, len(raw_text_idx) - 2):
        whole_left = [raw_text_idx[i - 2], raw_text_idx[i - 1], raw_text_idx[i]]
        whole_right = [raw_text_idx[i], raw_text_idx[i + 1], raw_text_idx[i + 2]]
        context_list.append(whole_left)
        context_list.append(whole_right)

    return context_list, word2idx_dic, idx2word_dic


def judge_word(candidate_list, context_list, word2idx_dic, idx2word_dic, test_path=None,  test_sentence=None):
    if test_path is not None:
        f2 = open(test_path, 'r', encoding='utf-8')
        print('Load test text……')

        sentence = []
        for line in f2.readlines():
            line = rm_useless_tokens(line).strip()
            for x in line:
                if x != ' ' and x != 9:
                    sentence.append(x)

        context_all = sentence
    
    if test_sentence is not None:
        context_all = test_sentence.strip().split()

    i = 0
    num = 0
    for index in range(len(context_all)):
        if context_all[index] in candidate_list:
            prop={}
            i += 1
            print('第{}处：'.format(i))
            if index > 2 and len(context_all)-index > 1:
                num = 3
                context_word = [context_all[index-2], context_all[index-1], context_all[index+1], context_all[index+2]]
                context = word2idx(context_word, word2idx_dic)
            elif index == 2:
                num = 2
                context_word = [context_all[index-1], context_all[index+1], context_all[index+2]]
                context = word2idx(context_word, word2idx_dic)
                context.insert(0,str(random.randint(1, 2000)))
            elif index ==1:
                num = 1
                context_word = [context_all[index+1], context_all[index+2]]
                context = word2idx(context_word, word2idx_dic)
                context.insert(0,str(random.randint(1, 2000)))
                context.insert(0,str(random.randint(1, 2000)))
            elif len(context_all)-index == 1:
                num = 3
                context_word = [context_all[index-2], context_all[index-1], context_all[index+1]]
                context = word2idx(context_word, word2idx_dic)
                context.insert(3,str(random.randint(1, 2000)))
                context.insert(3,str(random.randint(1, 2000)))
            elif len(context_all)-index == 0:
                num = 3
                context_word = [context_all[index-2], context_all[index-1]]
                context = word2idx(context_word, word2idx_dic)
                context.insert(2,str(random.randint(1, 2000)))
                context.insert(2,str(random.randint(1, 2000)))

            context_left1 = context[1:2]
            context_left2 = context[0:2]
            context_right1 = context[2:3]
            context_right2 = context[2:4]

            for candidate in candidate_list:
                # left_1
                whole_left1 = context_left1.copy()
                whole_left1.insert(1, str(word2idx_dic[candidate]))

                context_left1_num = context_list.count(context_left1)
                whole_left1_num = context_list.count(whole_left1)

                # right_1
                whole_right1 = context_right1.copy()
                whole_right1.insert(1, str(word2idx_dic[candidate]))

                context_right1_num = context_list.count(context_right1)
                whole_right1_num = context_list.count(whole_right1)
            
                # left_2
                whole_left2 = context_left2.copy()
                whole_left2.insert(2, str(word2idx_dic[candidate]))

                context_left2_num = context_list.count(context_left2)
                whole_left2_num = context_list.count(whole_left2)

                # right_2
                whole_right2 = context_right2.copy()
                whole_right2.insert(2, str(word2idx_dic[candidate]))

                context_right2_num = context_list.count(context_right2)
                whole_right2_num = context_list.count(whole_right2)

                # V是所有的可能的不同的N-Gram的数量
                V = len(context_list)
                # Add-k Smoothing（Lidstone’s law）  小于1的正数 k
                k = 0.5

                # sum e_yi
                # e_yi = sum(math.exp(x) for x in whole1_3)
                p_left1 = (whole_left1_num + k)/(context_left1_num + k*V)
                p_right1 = (whole_right1_num + k)/(context_right1_num + k*V)
                p_left2 = (whole_left2_num + k)/(context_left2_num + k*V)
                p_right2 = (whole_right2_num + k)/(context_right2_num + k*V)
                p = ( p_left1 +  p_left2 + p_right2 +  p_right2)/4
                prop[candidate] = p

            proplist = sorted(prop.items(),key = lambda x:x[1])
            
            if proplist[-1][1] == proplist[-2][1]:
                word = '不能确定是哪个字'
            else:
                word = proplist[-1][0]
            print('sentence "{0}" 中第{1}个字可能为: \033[1;33m{2}\033[0m'.format(''.join(context_word), num, word))


if __name__ == "__main__":
    
    # # 对训练文本进行分词
    # ChineseParticiple(RAW_TEXT_PATH, PARTED_TEXT_PATH)

    # # 生成字典并保存到本地
    # word_to_idx, idx_to_word = generate_dic(PARTED_TEXT_PATH)
    # save_dic(word_to_idx, WORD2IDX_PATH)
    # save_dic(idx_to_word, IDX2WORD_PATH)
    # # 以上内容执行一次之后，如果原始文本没有改变，就不用重复进行了

    # 载入
    context_list, word2idx_dic, idx2word_dic = load(PARTED_TEXT_PATH, WORD2IDX_PATH, IDX2WORD_PATH)
    judge_word(['人', '入'], context_list, word2idx_dic, idx2word_dic, test_path=TEST_PATH)
    # judge_word(raw_text, raw_text_idx, word2idx_dic, idx2word_dic, test_sentence='this is a sentence')



