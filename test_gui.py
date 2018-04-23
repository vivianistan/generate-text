#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This example shows how to use
a QComboBox widget.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

# Imports:
from PyQt5.Qt import *
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QApplication,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QLabel, QWidget)
from generate import get_links, get_text_local, count_and_prob_bigram, gen_next_word
import sys

import nltk
import random
import re
from nltk.corpus import brown
from nltk import word_tokenize
from nltk.util import ngrams
import random
import time

authors = ['Jane Austen', 'G.K. Chesterton', 'William Shakespeare', 'Sir Arthur Conan Doyle', 'Fyodor Dostoyevsky']
corpus_list = [[]]

def nltk_2gram(author1_index):
    global corpus_list
    tokens = corpus_list[author1_index][:]
    cfreq_pride_2gram = nltk.ConditionalFreqDist(nltk.bigrams(tokens))
    cprob_pride_2gram = nltk.ConditionalProbDist(cfreq_pride_2gram, nltk.MLEProbDist)
    word = tokens[random.randint(0, len(tokens))]
    print(word)
    t = ''
    word_count = 0
    for i in range(0,100):
        # print(word, end=' ')
        # Only add words that have alphanumeric characters
        valid = re.match('^[a-zA-Z.,-/?;:!0123456789]+', word) is not None
        if valid:
            t += re.match('^[a-zA-Z.,-/?;:!0123456789]+', word).group(0) + ' '
            print(word, end=' ')
            word = cprob_pride_2gram[word].generate()
            word_count += 1
            # print('word count :', word_count)
        else:
            print('*', word, end='* ')
            word = tokens[random.randint(0, len(tokens))]
            pass

    return t
    

def custom_2gram(author1_index):
    global corpus_list
    tokens = corpus_list[author1_index][:]
    count_dict = {}
    prob_dict = {}
    start = tokens[random.randint(0, len(tokens))]
    count_dict, prob_dict = count_and_prob_bigram(tokens, count_dict, prob_dict)
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

def custom_3gram(author1_index):
    global corpus_list
    index = authors.index(text)
    tokens = corpus_list[index][:]
    return authors[author1_index]


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
        self.combo3.addItem("NLTK-2gram")
        self.combo3.addItem("Custom-2gram")
        self.combo3.addItem("Custom-3gram")

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
        technique = ['NLTK-2gram', 'Custom-2gram', 'Custom-3gram']
        author1_index = authors.index(self.combo1.currentText())
        author2_index = authors.index(self.combo2.currentText())
        technique_index = technique.index(self.combo3.currentText())
        text = ''

        if technique_index == 0:
            text = nltk_2gram(author1_index)
        elif technique_index == 1:
            text = custom_2gram(author1_index)
        else:
            text = custom_3gram(author1_index)

        self.lbl.setText(text)
        self.lbl.setWordWrap(True);
        self.lbl.adjustSize()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())