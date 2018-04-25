#!/usr/bin/python3

# Imports:
import sys
import nltk
import random
import re
import random
import time
import numpy as np 

from PyQt5.Qt import *
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QApplication,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QLabel, QWidget)
from generate import get_links, get_text_local, count_and_prob_bigram, gen_next_word
from nltk import word_tokenize, trigrams, bigrams
from nltk.util import ngrams
from collections import Counter, defaultdict

authors = ['Jane Austen', 'G.K. Chesterton', 'William Shakespeare', 'Sir Arthur Conan Doyle', 'Fyodor Dostoyevsky']
corpus_list = [[]]

def nltk_2gram(author1_index):
    global corpus_list
    tokens = corpus_list[author1_index][:]
    cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(tokens))
    cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.MLEProbDist)
    word = tokens[random.randint(0, len(tokens))]
    # print(word)
    t = ''
    word_count = 0
    for i in range(0,100):
        # print(word, end=' ')
        # Only add words that have alphanumeric characters
        valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
        if valid:
            t += re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0) + ' '
            print(word, end=' ')
            word = cprob_2gram[word].generate()
            word_count += 1
            # print('word count :', word_count)
        else:
            print('*', word, end='* ')
            word = tokens[random.randint(0, len(tokens))]
            pass

    return t

def nltk_2gram_mix(author1_index, author2_index, ratio):
    global corpus_list

    tokens1 = corpus_list[author1_index][:]
    tokens2 = corpus_list[author2_index][:]

    print("in method:")
    print(authors[author1_index])
    print(authors[author2_index])
    
    cfreq_2gram1 = nltk.ConditionalFreqDist(nltk.bigrams(tokens1))
    cprob_2gram1 = nltk.ConditionalProbDist(cfreq_2gram1, nltk.MLEProbDist)
    print(cfreq_2gram1)
    print(cprob_2gram1)
    cfreq_2gram2 = nltk.ConditionalFreqDist(nltk.bigrams(tokens2))
    cprob_2gram2 = nltk.ConditionalProbDist(cfreq_2gram2, nltk.MLEProbDist)
    print(cfreq_2gram2)
    print(cprob_2gram2)

    r = random.randint(0,100)
    word = ''
    if r < ratio:
        word = tokens1[random.randint(0, len(tokens1))]
    else:
        word = tokens2[random.randint(0, len(tokens2))]
    # r = random.randint(0,100)
    print(word)
    t = ''
    word_count = 0
    for i in range(0,100):
        # print(word, end=' ')
        # Only add words that have alphanumeric characters
        valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
        if valid:
            t += re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0) + ' '
            # print(word, end=' ')
            if r > ratio:
                print(cprob_2gram1[word])
                if word not in tokens1:
                    word = tokens1[random.randint(0, len(tokens1))]
                word = cprob_2gram1[word].generate()
            else:
                if word not in tokens2:
                    word = tokens2[random.randint(0, len(tokens2))]
                print(cprob_2gram2[word])
                word = cprob_2gram2[word].generate()

            word_count += 1
            # print('word count :', word_count)
        else:
            print('*', word, end='* ')
            if r < ratio:
                word = tokens1[random.randint(0, len(tokens1))]
            else:
                word = tokens2[random.randint(0, len(tokens2))]

            
        r = random.randint(0,100)

    return t


def custom_2gram(author1_index):
    global corpus_list
    tokens = corpus_list[author1_index][:]
    count_dict = {}
    prob_dict = {}
    word = tokens[random.randint(0, len(tokens))]
    count_dict, prob_dict = count_and_prob_bigram(tokens, count_dict, prob_dict)
    t = ''
    for i in range(0,100):
        valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
        if valid:
            t += re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0) + ' '
            print(word, end=' ')
            word = gen_next_word(word, prob_dict)
        else:
            print('*', word, end='* ')
            word = tokens[random.randint(0, len(tokens))]
            pass

    return t

def custom_2gram_mix(author1_index, author2_index, ratio):
    global corpus_list
    tokens1 = corpus_list[author1_index][:]
    tokens2 = corpus_list[author1_index][:]
    count_dict1 = {}
    prob_dict1 = {}
    count_dict2 = {}
    prob_dict2 = {}
    word = tokens1[random.randint(0, len(tokens1))]
    count_dict, prob_dict = count_and_prob_bigram(tokens1, count_dict1, prob_dict1)
    count_dict, prob_dict = count_and_prob_bigram(tokens2, count_dict2, prob_dict2)
    t = ''
    for i in range(0,100):
        valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
        if valid:
            t += re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0) + ' '
            print(word, end=' ')
            r = random.randint(0,100)
            if r > ratio:
                if word not in tokens1:
                    word = tokens1[random.randint(0, len(tokens1))]
                word = gen_next_word(word, prob_dict1)
            else:
                if word not in tokens2:
                    word = tokens2[random.randint(0, len(tokens2))]
                word = gen_next_word(word, prob_dict2)
        else:
            print('*', word, end='* ')
            if r > ratio:
                word = tokens1[random.randint(0, len(tokens1))]
            else:
                word = tokens2[random.randint(0, len(tokens2))]

    return t

def markov_chain(author1_index):
    global corpus_list
    tokens = corpus_list[author1_index][:]
    bigrams = nltk.bigrams(tokens)
    word_dict = {}

    for word1, word2 in bigrams:
        if word1 in word_dict.keys():
            word_dict[word1].append(word2)
        else:
            word_dict[word1] = [word2]

    word = tokens[random.randint(0,len(tokens))]
    chain = []
    for i in range(0,100):
        valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
        if valid:
            chain.append(re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0))
            word = np.random.choice(word_dict[word])
        else:
            word = tokens[random.randint(0,len(tokens))]

    print(' '.join(chain))
    return (' '.join(chain))

def markov_chain_mix(author1_index, author2_index, ratio):
    global corpus_list
    tokens1 = corpus_list[author1_index][:]
    tokens2 = corpus_list[author2_index][:]
    bigrams1 = nltk.bigrams(tokens1)
    bigrams2 = nltk.bigrams(tokens2)
    word_dict1 = {}
    word_dict2 = {}

    for word1, word2 in bigrams1:
        if word1 in word_dict1.keys():
            word_dict1[word1].append(word2)
        else:
            word_dict1[word1] = [word2]

    for word1, word2 in bigrams2:
        if word1 in word_dict2.keys():
            word_dict2[word1].append(word2)
        else:
            word_dict2[word1] = [word2]

    word = tokens1[random.randint(0,len(tokens1))]
    chain = []
    r = random.randint(0,100)

    for i in range(0,100):
        valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
        if valid:
            chain.append(re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0))
            r = random.randint(0,100)
            if r > ratio:
                if word not in tokens1:
                    word = tokens1[random.randint(0, len(tokens1))]
                word = np.random.choice(word_dict1[word])
            else:
                if word not in tokens2:
                    word = tokens2[random.randint(0, len(tokens2))]
                word = np.random.choice(word_dict2[word])
        else:
            if r > ratio:
                word = tokens1[random.randint(0, len(tokens1))]
            else:
                word = tokens2[random.randint(0, len(tokens2))]

    print(' '.join(chain))
    return (' '.join(chain))


def nltk_3gram(author1_index):
    global corpus_list
    tokens = corpus_list[author1_index][:]
   
    # Too slow: 
    # padded_trigrams = trigrams(tokens, pad_left=True, pad_right=True)
    # model = defaultdict(lambda: defaultdict(lambda: 0))
 
    # for word in tokens:
    #     for w1, w2, w3 in trigrams(tokens, pad_right=True, pad_left=True):
    #         print(w1,w2,w3)
    #         model[(w1, w2)][w3] += 1

    # # Let's transform the counts to probabilities
    # for w1_w2 in model:
    #     total_count = float(sum(model[w1_w2].values()))
    #     for w3 in model[w1_w2]:
    #         model[w1_w2][w3] /= total_count

    # text = [None, None]
 
    # sentence_finished = False
    
    # # for i in range (0,100): 
    # while not sentence_finished:
    #     r = random.random()
    #     accumulator = .0
     
    #     for word in model[tuple(text[-2:])].keys():
    #         accumulator += model[tuple(text[-2:])][word]
     
    #         if accumulator >= r:
    #             text.append(word)
    #             break
     
    #     if text[-2:] == [None, None]:
    #         sentence_finished = True
     
    # print (' '.join([t for t in text if t]))
     
     
 
    # trigrams_as_bigrams.extend([((t[0],t[1]), t[2]) for t in trigrams])
    # cfd = nltk.ConditionalFreqDist(trigrams_as_bigrams)
    # # cpd = nltk.ConditionalProbDist(cfd, nltk.MLEProbDist)
    # print(cfd)
    # # print(cpd)
    # # condition_pairs = (((w0, w1), w2) for w0, w1, w2 in trigrams(tokens))
    # # cfd = nltk.ConditionalFreqDist(condition_pairs)
    # # # cfreq_pride_3gram = nltk.ConditionalFreqDist(trigrams(tokens))
    # # cprob_3gram = nltk.ConditionalProbDist(cfd, nltk.MLEProbDist)
    # # print(cprob_3gram)
    # word = tokens[random.randint(0, len(tokens))]
    # print(word)
    # t = ''
    # word_count = 0
    # for i in range(0,100):
    #     valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
    #     if valid:
    #         t += re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0) + ' '
    #         # print(word, end=' ')
    #         # word = cprob_3gram[word].generate()
    #         # word = content_model.generate(words_to_generate, starting_words)
    #         # print ("{0}: {1}".format(cpd[trigrams_as_bigrams[0]].prob(trigrams_as_bigrams[1]), trigrams_as_bigrams))
    #         # word = cpd[word].generate()
    #         print(cfd[word])
    #         word_count += 1
    #         # print('word count :', word_count)
    #     else:
    #         print('*', word, end='* ')
    #         word = tokens[random.randint(0, len(tokens))]
    #         pass

    # return t

def custom_3gram(author1_index):
    global corpus_list
    index = authors.index(text)
    tokens = corpus_list[index][:]
    count_dict = {}
    prob_dict = {}
    start = tokens[random.randint(0, len(tokens))]
    count_dict, prob_dict = count_and_prob_trigram(tokens, count_dict, prob_dict)
    word = start
    t = ''
    for i in range(0,100):
        valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
        if valid:
            t += re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0) + ' '
            print(word, end=' ')
            word = gen_next_word(word, prob_dict)
        else:
            print('*', word, end='* ')
            word = tokens[random.randint(0, len(tokens))]
            pass

    return t
    # return authors[author1_index]


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Init corpus
        global corpus_list
        corpus_list = [[]]
        time0 = time.time()

        # corpus_list = get_links(corpus_list)
        corpus_list = get_text_local(corpus_list)
        time1 = time.time()
        print('elapsed time: %d' % (time1-time0))
        print(len(corpus_list))

        # Make components:
        self.lbl = QLabel("Your text will be displayed here", self)
        self.combo1_lbl = QLabel("Author 1", self)
        self.combo2_lbl = QLabel("Author 2", self)
        self.combo3_lbl = QLabel("Technique", self)

        self.combo1 = QComboBox(self)
        self.combo1.addItem("Jane Austen")
        self.combo1.addItem("G.K. Chesterton")
        self.combo1.addItem("William Shakespeare")
        self.combo1.addItem("Sir Arthur Conan Doyle")
        self.combo1.addItem("Fyodor Dostoyevsky")

        self.combo2 = QComboBox(self)
        self.combo2.addItem("Jane Austen")
        self.combo2.addItem("G.K. Chesterton")
        self.combo2.addItem("William Shakespeare")
        self.combo2.addItem("Sir Arthur Conan Doyle")
        self.combo2.addItem("Fyodor Dostoyevsky")

        self.combo3 = QComboBox(self)
        self.combo3.addItem("NLTK-2gram (No mix, Author 1 only)")
        self.combo3.addItem("Custom-2gram (No mix, Author 1 only)")
        self.combo3.addItem("Markov Chain (No mix, Author 1 only)")
        self.combo3.addItem("NLTK-2gram mix")
        self.combo3.addItem("Custom-2gram mix")
        self.combo3.addItem("Markov Chain mix")
        

        self.a1_lbl = QLabel("Author 1", self)
        self.a2_lbl = QLabel("Author 2", self)

        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(11)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)

        self.button = QPushButton("Generate", self)

        # Add to layout
        grid = QGridLayout()
        grid.addWidget(self.combo1_lbl, 0, 0)
        grid.addWidget(self.combo2_lbl, 1, 0)
        grid.addWidget(self.combo3_lbl, 2, 0)
        grid.addWidget(self.combo1, 0, 1)
        grid.addWidget(self.combo2, 1, 1)
        grid.addWidget(self.combo3, 2, 1)

        grid.addWidget(self.a1_lbl, 3,0)
        grid.addWidget(self.slider, 3,1)
        grid.addWidget(self.a2_lbl, 3,2)
        grid.addWidget(self.button, 4,1)
        grid.addWidget(self.lbl,5,1)

        self.setLayout(grid)

        self.button.clicked.connect(self.onClick)

        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('Generate text')
        self.show()


    def onClick(self):
        global corpus_list
        technique = ['NLTK-2gram (No mix, Author 1 only)', 'Custom-2gram (No mix, Author 1 only)', 
                        'Markov Chain (No mix, Author 1 only)', 'NLTK-2gram mix', 'Custom-2gram mix', 'Markov Chain mix']
        print("button pushed")
        print(self.combo1.currentText())
        print(self.combo2.currentText())
        author1_index = authors.index(self.combo1.currentText())
        author2_index = authors.index(self.combo2.currentText())
        technique_index = technique.index(self.combo3.currentText())
        ratio = self.slider.value()
        text = ''
        print('First index: ', author1_index)

        if technique_index == 0:
            text = nltk_2gram(author1_index)
        elif technique_index == 1:
            text = custom_2gram(author1_index)
        elif technique_index == 2:
                text = markov_chain(author1_index)
        elif technique_index == 3:
            text = nltk_2gram_mix(author1_index, author2_index, ratio)
        elif technique_index == 4:
            text = custom_2gram_mix(author1_index, author2_index, ratio)
        else:
            text = markov_chain_mix(author1_index, author2_index, ratio)

        self.lbl.setText(text)
        self.lbl.setWordWrap(True);
        self.lbl.adjustSize()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())