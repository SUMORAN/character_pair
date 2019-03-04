import torch
from torch.autograd import Variable
import torch.nn as nn
import numpy as np


def make_context_vector(context, word_to_ix):
    # idxs = [word_to_ix[w] for w in context]
    idxs = []
    for w in context:
        try:
            idxs.append(word_to_ix[w])
        except KeyError:
            pass
    tensor = torch.LongTensor(idxs)
    return Variable(tensor)

def get_index_of_max(input):
    index = 0
    for i in range(1, len(input)):
        if input[i] > input[index]:
            index = i
    return index

def get_max_prob_result(input, ix_to_word):
    return ix_to_word[get_index_of_max(input)]

CONTEXT_SIZE = 2  # 2 words to the left, 2 to the right

EMDEDDING_DIM = 100

word_to_ix = {}

ix_to_word = {}

raw_text = """We are about to study the idea of a computational process.
Computational processes are abstract beings that inhabit computers.
As they evolve, processes manipulate other abstract things called data.
The evolution of a process is directed by a pattern of rules
called a program. People create programs to direct processes. In effect,
we conjure the spirits of the computer with our spells.""".split()

# f1 = open('parted_text_lines.txt', 'r', encoding='utf-8')
# print('Load raw text……')
# sentence = []
# num = 0
# for line in f1.readlines():
#     num += 1
#     if num > 100000:
#         break
#     if line != '':  # 去除空白行
#         sentence.append(line.strip())
#
# raw_text = sentence
# By deriving a set from `raw_text`, we deduplicate the array

vocab = set(raw_text)

vocab_size = len(vocab)

for i, word in enumerate(vocab):
    word_to_ix[word] = i

    ix_to_word[i] = word


class CBOW(torch.nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(CBOW, self).__init__()

        # out: 1 x emdedding_dim

        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        embeddings = self.embeddings
        print(embeddings)

        self.linear1 = nn.Linear(embedding_dim, 128)

        self.activation_function1 = nn.ReLU()

        # out: 1 x vocab_size

        self.linear2 = nn.Linear(128, vocab_size)

        self.activation_function2 = nn.LogSoftmax(dim=-1)

    def forward(self, inputs):
        # print('-------------------------')
        # print(inputs)
        embeds = sum(self.embeddings(inputs)).view(1, -1)

        out = self.linear1(embeds)

        out = self.activation_function1(out)

        out = self.linear2(out)

        out = self.activation_function2(out)

        return out

    def get_word_emdedding(self, word):
        word = Variable(torch.LongTensor([word_to_ix[word]]))

        return self.embeddings(word).view(1, -1)

def train(raw_text, vocab_size, EMDEDDING_DIM):
    data = []

    for i in range(3, len(raw_text) - 3):
        context = [raw_text[i - 3], raw_text[i - 2], raw_text[i - 1],

                   raw_text[i + 1], raw_text[i + 2], raw_text[i + 3]]

        target = raw_text[i]

        data.append((context, target))

    model = CBOW(vocab_size, EMDEDDING_DIM)

    loss_function = nn.NLLLoss()

    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

    for epoch in range(50):
        print('================')
        print('epoch {}'.format(epoch))
        total_loss = 0

        for context, target in data:
            context_vector = make_context_vector(context, word_to_ix)

            model.zero_grad()

            log_probs = model(context_vector)

            loss = loss_function(log_probs, Variable(

                torch.LongTensor([word_to_ix[target]])))

            loss.backward()

            optimizer.step()

            total_loss += loss.data

    # 仅保存模型参数
    torch.save(model.state_dict(), 'model.pkl')


# ====================== TRAIN
train(raw_text, vocab_size, EMDEDDING_DIM)

# ====================== TEST

context = ['We', 'study', 'the', 'of', 'a', 'process']
# context = ['我', '来', '说', '句', '广', '州', '男']

context_vector = make_context_vector(context, word_to_ix)

# 加载模型参数
trained_model = CBOW(vocab_size, EMDEDDING_DIM)
trained_model.load_state_dict(torch.load('model.pkl'))
a = trained_model(context_vector).data.numpy()
print('a:')
print(a)

candidate_1 = 'idea'
candidate_1_embed = trained_model.get_word_emdedding(candidate_1).numpy()
print(candidate_1_embed)

print('Raw text: {}\n'.format(' '.join(raw_text)))

print('Context: {}\n'.format(context))

print('Prediction: {}'.format(get_max_prob_result(a[0], ix_to_word)))