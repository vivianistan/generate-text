# Imports: 
import nltk
import random
from nltk.corpus import brown
from nltk import word_tokenize
from nltk.util import ngrams
import random
from urllib import request
import re
import os
import glob
import io
import encodings
import pkgutil
import csv

austen_corpus =  ''
chesterson_corpus = ''


# Returns counts and probabilities of a corpus using bigrames
def count_and_prob_bigram(corpus, count, prob):
	count2 = {}
	# Count bigrams and instantiate probability for each word to 0
	for word1, word2 in nltk.bigrams(corpus):
	    if word1 not in count:
	        count[word1] = { }
	        count2[word1] = 0
	        prob[word1] = {}

	    if word2 not in count[word1]:
	    	#print(word1, word2)
	    	count[word1][word2] = 1
	    	count2[word1] += 1
	    else:
	        count[word1][word2] += 1
	        count2[word1] += 1

	# Recall: To estimate probabilities of bigrams: 
	# P(word2|word1) = count(word1, word2)/count(word1, ...)

	# for each word, calculate probability of bigram(s)
	for word1 in count:
		for word2 in count[word1]:
			# print(word1, word2,':', count[word1][word2]/count2[word1])
			prob[word1][word2] = count[word1][word2]/count2[word1]

	return count, prob


# get the next word based on probabilities
def gen_next_word(word, prob_dict):
	boundary = []
	words = []
	count = 0

	# Generate random number
	dart = random.random()

	if(len(prob_dict) == 0): return 'ERROR'

	# Get probabilities and words
	for w in prob_dict[word]:
		# get first probability and first word
		boundary.append(prob_dict[word][w])
		words.append(w)
		count += 1

	#print('boundary:',boundary)
	#print('words:', words)

	# return the next word based on the dart value and boundaries
	# if there is only one option, return the word:
	if count == 1:
		return words[0]
	else:
		#if there are more options, find the minimum
		#sort lists together 
		boundary, words = (list(t) for t in zip(*sorted(zip(boundary, words))))

		# go through boundaries, starting with smallest 
		# (Note: though this assignment could be completed w/a simple if else, 
		# I wanted to try and write code that could work with trigrams and up)
		total = 0;
		for i in range(0,len(boundary)):
			if i==0:
				total = boundary[i]
				if dart<=total:
					return words[i]
			# add previous probabilities 
			elif dart<=(boundary[i]+total):
					return words[i]
			else:
				total += boundary[i]
				# print('look again')

'''
	Fills an empty list with the corpuses of the 5 authores
'''
def get_links(complete_corpus): 

	austen_links = ["http://www.gutenberg.org/cache/epub/42671/pg42671.txt",
	               "https://www.gutenberg.org/files/1212/1212-0.txt", "https://www.gutenberg.org/files/141/141-0.txt", 
	                "https://www.gutenberg.org/files/121/121-0.txt", 
	                "http://www.gutenberg.org/cache/epub/161/pg161.txt", "http://www.gutenberg.org/cache/epub/946/pg946.txt"]

	#response = request.urlopen(url)

	austen_corpus = []

	for link in austen_links: 
	    response = request.urlopen(link)
	    text = response.read().decode('utf8')
	    tokens = nltk.word_tokenize(text)
	    austen_corpus.append(tokens)

	complete_corpus.append(austen_corpus)
	# austen_corpus[:100]

	# G.K. Chesterton
	chesterton_links = ["http://www.gutenberg.org/files/1717/1717-0.txt", "http://www.gutenberg.org/cache/epub/11505/pg11505.txt", 
	                   'http://www.gutenberg.org/cache/epub/1720/pg1720.txt','http://www.gutenberg.org/cache/epub/20897/pg20897.txt',
	                   'http://www.gutenberg.org/cache/epub/11339/pg11339.txt', 'http://www.gutenberg.org/cache/epub/470/pg470.txt',
	                   'https://www.gutenberg.org/files/16769/16769-0.txt','https://www.gutenberg.org/files/5265/5265-0.txt']

	chesterton_corpus = [] 
	                
	for link in chesterton_links: 
	    response = request.urlopen(link)
	    text += response.read().decode('utf8')
	    tokens = nltk.word_tokenize(text)
	    chesterton_corpus.append(tokens)

	complete_corpus.append(chesterton_corpus)
	# Shakespeare Complete works:
	
	shakespeare_corpus = []
	 
	shakespeare_links = ['https://www.gutenberg.org/files/100/100-0.txt']

	for link in shakespeare_links: 
	    response = request.urlopen(link)
	    text += response.read().decode('utf8')
	    tokens = nltk.word_tokenize(text)
	    shakespeare_corpus.append(tokens)

	complete_corpus.append(shakespeare_corpus)   					
	# Sir Arthur Conan Doyle
	doyle_links = ['http://www.gutenberg.org/cache/epub/1661/pg1661.txt','https://www.gutenberg.org/files/2852/2852-0.txt',
	              'https://www.gutenberg.org/files/244/244-0.txt', 'http://www.gutenberg.org/cache/epub/2097/pg2097.txt',
	              'https://www.gutenberg.org/files/834/834-0.txt', 'https://www.gutenberg.org/files/108/108-0.txt', 
	              'http://www.gutenberg.org/cache/epub/139/pg139.txt', 'https://www.gutenberg.org/files/3289/3289-0.txt']

	doyle_corpus = []

	for link in doyle_links: 
	    response = request.urlopen(link)
	    text += response.read().decode('utf8')
	    tokens = nltk.word_tokenize(text)
	    doyle_corpus.append(tokens)

	complete_corpus.append(doyle_corpus)
	# Fyodor Doestevsky 
	doestevsky_links = ['https://www.gutenberg.org/files/28054/28054-0.txt', 'http://www.gutenberg.org/cache/epub/600/pg600.txt', 
	                   'https://www.gutenberg.org/files/2638/2638-0.txt', 'http://www.gutenberg.org/cache/epub/8578/pg8578.txt',
	                   'https://www.gutenberg.org/files/8117/8117-0.txt','http://www.gutenberg.org/cache/epub/36034/pg36034.txt',
	                   'https://www.gutenberg.org/files/2302/2302-0.txt', 'https://www.gutenberg.org/files/2554/2554-0.txt']

	doestevsky_corpus = []                   

	for link in doestevsky_links: 
	    response = request.urlopen(link)
	    text += response.read().decode('utf8')
	    tokens = nltk.word_tokenize(text)
	    dostevsky_corpus.append(tokens)

	complete_corpus.append(dostevsky_corpus)
	return complete_corpus


def all_encodings():
    modnames = set(
        [modname for importer, modname, ispkg in pkgutil.walk_packages(
            path=[os.path.dirname(encodings.__file__)], prefix='')])
    aliases = set(encodings.aliases.aliases.values())
    return modnames.union(aliases)


# TODO: Preprocessing
# 	* remove headers/footers/links/non-english characters
# 	* check formatting? (Dostoyevsky?)

def get_text_local(complete_corpus): 
	authors = ['Jane Austen', 'G.K. Chesterton', 'William Shakespeare', 'Sir Arthur Conan Doyle', 'Fyodor Dostoyevsky']
	
	# Could streamline this to loops later? 
	# complete_corpus = [[]]
	count = 0

	path = '/Users/viviantan/Documents/Spring2018/LIN_353C/Project/texts/austen/'
	austen_tokens = []
	for filename in os.listdir(path):
		file_content = open(path+filename, encoding='cp437').read()
		tokens = nltk.word_tokenize(file_content)
		austen_tokens += tokens

	complete_corpus[count] += austen_tokens
	count += 1

	path = '/Users/viviantan/Documents/Spring2018/LIN_353C/Project/texts/chesterton/'
	chesterton_tokens = []
	encodings = all_encodings()
	for filename in os.listdir(path):
		# print(filename)
		# for enc in encodings:
		#     try:
		#         with open(path+filename, encoding=enc) as f:
		#             # print the encoding and the first 500 characters
		#             print(enc, f.read(200))
		#     except Exception:
  #       		pass
        #cp437
		file_content = open(path+filename, encoding='cp437').read()
		tokens = nltk.word_tokenize(file_content)
		chesterton_tokens += tokens

	# complete_corpus[count] += chesterton_tokens
	complete_corpus.append(chesterton_tokens)
	count += 1
	path = '/Users/viviantan/Documents/Spring2018/LIN_353C/Project/texts/shakespeare/'
	shakespeare_tokens = []
	for filename in os.listdir(path):
		# file_content = open(path+filename).read()
		file_content = open(path+filename, encoding='cp437').read()
		tokens = nltk.word_tokenize(file_content)
		shakespeare_tokens += tokens

	complete_corpus.append(shakespeare_tokens)
	# complete_corpus += shakespeare_tokens
	count += 1
	path = '/Users/viviantan/Documents/Spring2018/LIN_353C/Project/texts/doyle/'
	doyle_tokens = []
	for filename in os.listdir(path):
		# file_content = open(path+filename).read()
		file_content = open(path+filename, encoding='cp437').read()
		tokens = nltk.word_tokenize(file_content)
		doyle_tokens += tokens

	# complete_corpus[count] += doyle_tokens
	complete_corpus.append(doyle_tokens)

	count += 1
	path = '/Users/viviantan/Documents/Spring2018/LIN_353C/Project/texts/dostoyevsky/'
	dostoyevsky_tokens = []
	for filename in os.listdir(path):
		# file_content = open(path+filename).read()
		file_content = open(path+filename, encoding='cp437').read()
		tokens = nltk.word_tokenize(file_content)
		dostoyevsky_tokens += tokens

	complete_corpus.append(dostoyevsky_tokens)

	print(len(complete_corpus))

	# with open("complete_corpus.csv", "wb") as f:
	#     writer = csv.writer(f)
	#     writer.writerows(complete_corpus)

	return complete_corpus
	# complete_corpus[count] += dostoyevsky_tokens






