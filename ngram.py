import nltk

from nltk.corpus import brown
from nltk import word_tokenize
from nltk.util import ngrams
import random

# an nltk.FreqDist() is like a dictionary,
# but it is ordered by frequency.
# Also, nltk automatically fills the dictionary
# with counts when given a list of words.

freq_brown = nltk.FreqDist(brown.words())


# Not a lot of variety. We need a bigger corpus.
# What kind of genres do we have in the Brown corpus?
print(brown.categories())
print("\n")

# Let's try Science Fiction.
cfreq_scifi = nltk.ConditionalFreqDist(nltk.bigrams(brown.words(categories = "science_fiction")))
cprob_scifi = nltk.ConditionalProbDist(cfreq_scifi, nltk.MLEProbDist)

word = "in"
for index in range(50):
    if index%3==0:
        word = cprob_scifi[ word ].generate()
    else:
        word = cprob_scifi[ word ].max()
    print(word, end = " ")

print("\n")

# # Let's try Science Fiction.
# cfreq_adv = nltk.ConditionalFreqDist(nltk.bigrams(brown.words(categories = "science_fiction")))
# cprob_adv = nltk.ConditionalProbDist(cfreq_adv, nltk.MLEProbDist)

# word = "in"
# for index in range(50):
#     word = cprob_scifi[ word ].generate()
#     print(word, end = " ")

# print("\n")

# try this with other Brown corpus categories.


# Let's try Science Fiction.
cfreq_adv = nltk.ConditionalFreqDist(nltk.bigrams(brown.words(categories = "adventure")))
cprob_adv = nltk.ConditionalProbDist(cfreq_adv, nltk.MLEProbDist)



word = "in"
for index in range(50):
    word = cprob_adv[ word ].generate()
    print(word, end = " ")

print("\n")

# Here is how to do this with NLTK books:
import nltk
from nltk.book import *

def generate_text(text, initialword, numwords):
    bigrams = list(nltk.ngrams(text, 2))
    cpd = nltk.ConditionalProbDist(nltk.ConditionalFreqDist(bigrams), nltk.MLEProbDist)
    word = initialword
    for i in range(numwords):
        print(word, end = " ")
        word = cpd[ word].generate()
    print(word) 

# Holy Grail
generate_text(text9, "I", 100)
# sense and sensibility
#generate_text(text2, "I", 100)

