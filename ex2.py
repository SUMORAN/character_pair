# -*- encoding: utf-8 -*-
import math
import random
import codecs

RAW_TEXT_PATH = "Tencent_AILab_ChineseEmbedding.txt" # 未分词中文语料
PARTED_TEXT_PATH = "parted_text.txt" # 分词后中文语料
WORD2IDX_PATH = 'word2idx_dic.txt'
IDX2WORD_PATH = 'idx2word_dic.txt'
TEST_PATH = 'test.txt'
PROP_DICT_PATH = 'prop_dict.txt'
similar_word = [
    "哀", "衰", "衷",
    "嗳", "暧", "暖"
    "巴", "巳",
    "拔", "拨",
    "斑", "班",
    "人", "入",
    "一", "-",
    "二", "=",
    "戋", "践",
    "己", "已",
    "候", "侯",
    "日", "曰",
    "间", "问",
    "央", "决",
    '粤', "粵"
]


# 移除每行文本中的无用词语和标点
def rm_useless_tokens(line):
    new_line = line.replace('.', '').replace('（', '').replace('）', '')\
        .replace('？', ' ').replace('！', ' ').replace('/', '').replace('，', '').replace('@', '')\
        .replace("\"", " ").replace("：", " ").replace('【', '').replace('】', '').replace('+', '')\
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
    for line in f:
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
        if lineNum > 880000:
            break
        

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
    for line in f1:
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
功能：根据训练语料生成概率字典
参数：
    parted_text_path: 分词后文件路径
    word2idx_path： word to idx 字典路径
    save_path： 生成的字典保存路径
'''
def generate_propdic(parted_text_path, word2idx_path, wordlist, save_path):
    raw_text = load_rawText(parted_text_path)
    word2idx_dic = load_dic(word2idx_path)
    raw_text_idx = word2idx(raw_text, word2idx_dic)
    prop_dict = {}
    
    print('正在计算context_single')
    # 考虑单边
    context_single = []
    # window = 0
    for i in range(0, len(raw_text_idx) - 1):
        whole = [raw_text_idx[i]]
        context_single.append(whole)

    # window = 1
    for i in range(1, len(raw_text_idx) - 1):
        whole_left = [raw_text_idx[i - 1], raw_text_idx[i]]
        whole_right = [raw_text_idx[i], raw_text_idx[i + 1]]
        context_single.append(whole_left)
        context_single.append(whole_right)

    # window = 2
    for i in range(2, len(raw_text_idx) - 2):
        whole_left = [raw_text_idx[i - 2], raw_text_idx[i - 1], raw_text_idx[i]]
        whole_right = [raw_text_idx[i], raw_text_idx[i + 1], raw_text_idx[i + 2]]
        context_single.append(whole_left)
        context_single.append(whole_right)
    
    print('正在计算context_double')
    # 考虑双边
    context_double = []
    whole_double = []
    # window = 1
    for i in range(1, len(raw_text_idx) - 1):
        whole = [raw_text_idx[i - 1], raw_text_idx[i], raw_text_idx[i + 1]]
        context_temp = [raw_text_idx[i - 1], raw_text_idx[i + 1]]
        whole_double.append(whole)
        context_double.append(context_temp)

    # window = 2
    for i in range(2, len(raw_text_idx) - 2):
        whole = [raw_text_idx[i - 2], raw_text_idx[i - 1], raw_text_idx[i],

                raw_text_idx[i + 1], raw_text_idx[i + 2]]
        context_temp = [raw_text_idx[i - 2], raw_text_idx[i - 1],

                raw_text_idx[i + 1], raw_text_idx[i + 2]]
        whole_double.append(whole)
        context_double.append(context_temp)


    wordlist = word2idx(wordlist, word2idx_dic)
    # V是所有的可能的不同的N-Gram的数量
    V1 = len(context_single)
    V2 = len(context_double)
    # Add-k Smoothing（Lidstone’s law）  小于1的正数 k
    k = 0.1
    hasdone = []
    for i in range(0, len(raw_text_idx)):
        if raw_text_idx[i] in wordlist:
            if raw_text_idx[i] not in hasdone:
                print('------------------------------')
                print('正在计算“{}”相关词的概率'.format(raw_text[i]))
                prop_dict[raw_text_idx[i]] = (context_single.count([raw_text_idx[i]])+k)/V1
                # 左边有两个字及以上
                if i > 1:
                    # 单边左
                    prop_dict[raw_text_idx[i-1],raw_text_idx[i]] =  (context_single.count([raw_text_idx[i-1],raw_text_idx[i]]) + \
                        k)/(context_single.count([raw_text_idx[i-1]]) + k*V1)
                    print('prop_dict[raw_text_idx[i-1],raw_text_idx[i]]:',prop_dict[raw_text_idx[i-1],raw_text_idx[i]])
                    prop_dict[raw_text_idx[i-2],raw_text_idx[i-1],raw_text_idx[i]] = (context_single.count([raw_text_idx[i-2],raw_text_idx[i-1],raw_text_idx[i]]) + k)/(context_single.count([raw_text_idx[i-2],raw_text_idx[i-1]]) + k*V1)
                    print(' prop_dict[raw_text_idx[i-2],raw_text_idx[i-1],raw_text_idx[i]]:', prop_dict[raw_text_idx[i-2],raw_text_idx[i-1],raw_text_idx[i]])
                    # 右边有两个字及以上
                    if i < len(raw_text_idx)-2 :
                        # 单边右
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1]]) + \
                            k)/(context_single.count([raw_text_idx[i+1]]) + k*V1)
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1],raw_text_idx[i+2]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1],\
                            raw_text_idx[i+2]]) + k)/(context_single.count([raw_text_idx[i+1],raw_text_idx[i+2]]) + k*V1)
                        # 双边
                        prop_dict[raw_text_idx[i-1],raw_text_idx[i],raw_text_idx[i+1]] = (whole_double.count([raw_text_idx[i-1],raw_text_idx[i],\
                            raw_text_idx[i+1]]) + k)/(context_double.count([raw_text_idx[i - 1], raw_text_idx[i + 1]]) + k*V2)
                        prop_dict[raw_text_idx[i - 2], raw_text_idx[i - 1], raw_text_idx[i], raw_text_idx[i + 1], raw_text_idx[i + 2]]\
                            = (whole_double.count( [raw_text_idx[i - 2], raw_text_idx[i - 1], raw_text_idx[i],raw_text_idx[i + 1], raw_text_idx[i + 2]])\
                            + k)/(context_double.count( [raw_text_idx[i - 2], raw_text_idx[i - 1], raw_text_idx[i + 1], raw_text_idx[i + 2]]) + k*V2)
                    # 右边只有一个字
                    elif i == len(raw_text_idx)-2 :
                        # 单边右
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1]]) + \
                            k)/(context_single.count([raw_text_idx[i+1]]) + k*V1)
                        # 双边
                        prop_dict[raw_text_idx[i-1],raw_text_idx[i],raw_text_idx[i+1]] = (whole_double.count([raw_text_idx[i-1],raw_text_idx[i],\
                            raw_text_idx[i+1]]) + k)/(context_double.count([raw_text_idx[i - 1], raw_text_idx[i + 1]]) + k*V2)
                    # 右边没有字了
                    else:
                        pass
                # 左边只有一个字
                elif i == 1:
                    # 单边左
                    prop_dict[raw_text_idx[i-1],raw_text_idx[i]] =  (context_single.count([raw_text_idx[i-1],raw_text_idx[i]]) + \
                        k)/(context_single.count([raw_text_idx[i-1]]) + k*V1)
                    # 双边
                    prop_dict[raw_text_idx[i-1],raw_text_idx[i],raw_text_idx[i+1]] = (whole_double.count([raw_text_idx[i-1],raw_text_idx[i],\
                        raw_text_idx[i+1]]) + k)/(context_double.count([raw_text_idx[i - 1], raw_text_idx[i + 1]]) + k*V2)
                    # 右边有两个字及以上
                    if i < len(raw_text_idx)-2 :
                        # 单边右
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1]]) + \
                            k)/(context_single.count([raw_text_idx[i+1]]) + k*V1)
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1],raw_text_idx[i+2]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1],\
                            raw_text_idx[i+2]]) + k)/(context_single.count([raw_text_idx[i+1],raw_text_idx[i+2]]) + k*V1)
                    # 右边只有一个字
                    elif i == len(raw_text_idx)-2 :
                        # 单边右
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1]]) + k)/(\
                            context_single.count([raw_text_idx[i+1]]) + k*V1)
                    else:
                        pass
                # 左边没有字了
                elif i == 0:
                # 右边有两个字及以上
                    if i < len(raw_text_idx)-2 :
                        # 单边右
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1]]) + \
                            k)/(context_single.count([raw_text_idx[i+1]]) + k*V1)
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1],raw_text_idx[i+2]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1],\
                            raw_text_idx[i+2]]) + k)/(context_single.count([raw_text_idx[i+1],raw_text_idx[i+2]]) + k*V1)
                    # 右边只有一个字
                    elif i == len(raw_text_idx)-2 :
                        # 单边右
                        prop_dict[raw_text_idx[i],raw_text_idx[i+1]] =  (context_single.count([raw_text_idx[i],raw_text_idx[i+1]]) + \
                            k)/(context_single.count([raw_text_idx[i+1]]) + k*V1)
                else:
                    pass      
                hasdone.append(raw_text_idx[i])

    save_dic(prop_dict, save_path)



def load(word2idx_path, prop_dict_path):
    print('载入概率字典----')
    word2idx_dic = load_dic(word2idx_path)
    prop_dict = load_dic(prop_dict_path)

    return word2idx_dic, prop_dict
    

def judge_word(candidate_list, prop_dict_path, word2idx_path, test_path=None,  test_sentence=None):
    print('Start judge-------------------')
    if test_path is not None:
        f2 = open(test_path, 'r', encoding='utf-8')
        print('Load test text……')

        sentence = []
        for line in f2.readlines():
            # line = rm_useless_tokens(line).strip()
            for x in line:
                if x != ' ' and x != '':
                    sentence.append(x)

        context_all = sentence
    
    if test_sentence is not None:
        context_all = test_sentence.strip().split()

    context_idx = word2idx(context_all, word2idx_dic)
    i = 0
    num = 0
    left = 0
    right = 0
    for index in range(len(context_all)):      
        if context_all[index] in candidate_list:
            prop={}
            i += 1
            print('第{}处：'.format(i))
            if index > 1 and index > len(context_all)-2:
                num = 3
                left = 2
                right = 2
            elif index == 1:
                num = 2
                left = 1
                if index > len(context_all)-2:
                    right = 2
                elif index == len(context_all)-2:
                    right = 1
                elif index == len(context_all)-1:
                    right = 0
            elif index == 0:
                num = 1
                left = 0
                if index > len(context_all)-2:
                    right = 2
                elif index == len(context_all)-2:
                    right = 1
                elif index == len(context_all)-1:
                    right = 0
            for candidate in candidate_list:
                if left == 2 and right == 2:
                    p = (prop_dict_path[context_idx[index]]
                                        + prop_dict_path[context_idx[index-1],context_idx[index]]
                                        + prop_dict_path[context_idx[index],context_idx[index+1]] 
                                        + prop_dict_path[context_idx[index-2],context_idx[index-1],context_idx[index]]
                                        + prop_dict_path[context_idx[index],context_idx[index+1],context_idx[index+2]] 
                                        + prop_dict_path[context_idx[index-1],context_idx[index],context_idx[index+1]]
                                        + prop_dict_path[context_idx[index-2],context_idx[index-1],context_idx[index],context_idx[index+1],context_idx[index+2]]
                                        )/7
                elif left == 1 and right == 2:
                    p = (prop_dict_path[context_idx[index]] 
                                        + prop_dict_path[context_idx[index-1],context_idx[index]] 
                                        + prop_dict_path[context_idx[index],context_idx[index+1]] 
                                        + prop_dict_path[context_idx[index],context_idx[index+1],context_idx[index+2]] 
                                        + prop_dict_path[context_idx[index-1],context_idx[index],context_idx[index+1]] 
                                        )/5
                elif left == 1 and right == 1:
                    p = (prop_dict_path[context_idx[index]] 
                                    + prop_dict_path[context_idx[index-1],context_idx[index]] 
                                    + prop_dict_path[context_idx[index],context_idx[index+1]] 
                                    + prop_dict_path[context_idx[index-1],context_idx[index],context_idx[index+1]] 
                                    )/4
                elif left == 1 and right == 0:
                    p = (prop_dict_path[context_idx[index]] 
                                    + prop_dict_path[context_idx[index-1],context_idx[index]] 
                                    )/2
                elif left == 0 and right == 2:
                    p = (prop_dict_path[context_idx[index]] 
                                        + prop_dict_path[context_idx[index],context_idx[index+1]] 
                                        + prop_dict_path[context_idx[index],context_idx[index+1],context_idx[index+2]] 
                                        )/3
                elif left == 0 and right == 1:
                    p = (prop_dict_path[context_idx[index]] 
                                        + prop_dict_path[context_idx[index],context_idx[index+1]] 
                                        )/2
                elif left == 0 and right == 0:
                    p = prop_dict_path[context_idx[index]] 
                                        
                prop[candidate] = p
            
            proplist = sorted(prop.items(),key = lambda x:x[1])
    
            if proplist[-1][1] == proplist[-2][1]:
                word = '不能确定是哪个字'
            else:
                word = proplist[-1][0]
            print('sentence "{0}" 中第{1}个字可能为: \033[1;33m{2}\033[0m'.format(context_all[index], num, word))


if __name__ == "__main__":
    
    # 对训练文本进行分词
    # print('开始分词')
    # ChineseParticiple(RAW_TEXT_PATH, PARTED_TEXT_PATH)

    # 生成字典并保存到本地
    print('开始生成字典')
    word_to_idx, idx_to_word = generate_dic(PARTED_TEXT_PATH)
    print('保存字典到本地')
    save_dic(word_to_idx, WORD2IDX_PATH)
    save_dic(idx_to_word, IDX2WORD_PATH)
    # generate_propdic(PARTED_TEXT_PATH, WORD2IDX_PATH, similar_word, PROP_DICT_PATH)
    # # 以上内容执行一次之后，如果原始文本没有改变，就不用重复进行了

    # # 载入
    # word2idx_dic, prop_dict = load(WORD2IDX_PATH, PROP_DICT_PATH)
    # judge_word(['人', '入'], prop_dict, word2idx_dic, test_path=TEST_PATH)
    # # judge_word(['人', '入'], prop_dict, word2idx_dic, test_sentence='this is a sentence')

