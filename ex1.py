# -*- encoding: utf-8 -*-
import math
import random


f1 = open('parted_text_lines.txt', 'r', encoding='utf-8')
print('Load raw text……')
sentence = []
num = 0
for line in f1.readlines():
    num += 1
    if num > 100000:
        break
    if line != '' and line != '9':  # 去除空白行
        sentence.append(line.strip())

raw_text = sentence

# raw_text = """We are about to study the idea of a computational process.
# Computational processes are abstract beings that inhabit computers.
# As they evolve, processes manipulate other abstract things called data.
# The evolution of a process is directed by a pattern of rules
# called a program. People create programs to direct processes. In effect,
# we conjure the spirits of the computer with our spells.
# We to study the idea of a computational process.""".split()

word_to_ix = {}
ix_to_word = {}

vocab = set(raw_text)
vocab_size = len(vocab)

# word to idx
for i, word in enumerate(vocab):
    word_to_ix[word] = i

    ix_to_word[i] = word

# 将原文字替换为对应idx
def word2idx(raw_text, word_to_ix):
    raw_text_idx = []
    for item in raw_text:
        if item in word_to_ix:
            item = item.replace(item, str(word_to_ix[item]))
        else:
            item = item.replace(item, str(random.randint(1, 500)))
        raw_text_idx.append(item)
    return raw_text_idx

raw_text = word2idx(raw_text, word_to_ix)

whole_list = []
context_list = []
# window = 1
for i in range(1, len(raw_text) - 1):
    whole = [raw_text[i - 1], raw_text[i], raw_text[i + 1]]
    context_temp = [raw_text[i - 1], raw_text[i + 1]]
    whole_list.append(whole)
    context_list.append(context_temp)

# window = 2
for i in range(2, len(raw_text) - 2):
    whole = [raw_text[i - 2], raw_text[i - 1], raw_text[i],

             raw_text[i + 1], raw_text[i + 2]]
    context_temp = [raw_text[i - 2], raw_text[i - 1],

               raw_text[i + 1], raw_text[i + 2]]
    whole_list.append(whole)
    context_list.append(context_temp)

# window = 3
for i in range(3, len(raw_text) - 3):
    whole = [raw_text[i - 3], raw_text[i - 2], raw_text[i - 1], raw_text[i],

             raw_text[i + 1], raw_text[i + 2], raw_text[i + 3]]
    context_temp = [raw_text[i - 3], raw_text[i - 2], raw_text[i - 1],

               raw_text[i + 1], raw_text[i + 2], raw_text[i + 3]]
    whole_list.append(whole)
    context_list.append(context_temp)



f2 = open('parted_test1_lines.txt', 'r', encoding='utf-8')
print('Load test text……')
sentence = []
num = 0
for line in f2.readlines():
    num += 1
    if num > 100000:
        break
    if line != '' and line != '9':  # 去除空白行
        sentence.append(line.strip())

context_all = sentence

# context = ['我', '来', '说', '句', '广', '州']
# context = ['to', 'study', 'the', 'of', 'a', 'computational']
i = 0
for index in range(len(context_all)):
    if context_all[index] == '人' or context_all[index] == '入':
        i += 1
        print('第{}处：'.format(i))
        context_word = [context_all[index-3], context_all[index-2], context_all[index-1], context_all[index+1], context_all[index+2], context_all[index+3]]
        context = word2idx(context_word, word_to_ix)
        context_1 = context[2:4]
        context_2 = context[1:5]
        candidate1 = '人'
        candidate2 = '入'

        print(word_to_ix[candidate1])

        whole1_3 = context.copy()
        whole2_3 = context.copy()
        whole1_3.insert(3, str(word_to_ix[candidate1]))
        whole2_3.insert(3, str(word_to_ix[candidate2]))

        context_3_num = context_list.count(context)
        whole1_3_num = whole_list.count(whole1_3)
        whole2_3_num = whole_list.count(whole2_3)

        whole1_2 = context_2.copy()
        whole2_2 = context_2.copy()
        whole1_2.insert(2, str(word_to_ix[candidate1]))
        whole2_2.insert(2, str(word_to_ix[candidate2]))

        context_2_num = context_list.count(context_2)
        whole1_2_num = whole_list.count(whole1_2)
        whole2_2_num = whole_list.count(whole2_2)

        whole1_1 = context_1.copy()
        whole2_1 = context_1.copy()
        whole1_1.insert(1, str(word_to_ix[candidate1]))
        whole2_1.insert(1, str(word_to_ix[candidate2]))

        context_1_num = context_list.count(context_1)
        whole1_1_num = whole_list.count(whole1_1)
        whole2_1_num = whole_list.count(whole2_1)


        # V是所有的可能的不同的N-Gram的数量
        V = len(context_list)
        # Add-k Smoothing（Lidstone’s law）  小于1的正数 k
        k = 0.5

        # sum e_yi
        # e_yi = sum(math.exp(x) for x in whole1_3)
        p1_3 = (whole1_3_num + k)/(context_3_num + k*V)
        p2_3 = (whole2_3_num + k)/(context_3_num + k*V)

        p1_2 = (whole1_2_num + k)/(context_2_num + k*V)
        p2_2 = (whole2_2_num + k)/(context_2_num + k*V)

        p1_1 = (whole1_1_num + k)/(context_1_num + k*V)
        p2_1 = (whole2_1_num + k)/(context_1_num + k*V)

        p1 = (p1_3 + p1_2 + p1_1)/3
        p2 = (p2_3 + p2_2 + p2_1)/3
        prop = p1/p2

        if prop > 10:
            word = candidate1
        elif prop < 0.1:
            word = candidate2
        else:
            word = '不能确定是哪个字'
        print('p1:{}'.format(p1))
        print('p2:{}'.format(p2))
        print('prop:{}'.format(prop))
        print('sentence "{0}" 中第4个字为: \033[1;33m{1}\033[0m'.format(''.join(context_word), word))

