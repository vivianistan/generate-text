# Imports: 
import nltk
import random
from nltk.corpus import brown
from nltk import word_tokenize
from nltk.util import ngrams
import random
from urllib import request
import re

austen_corpus =  ''
chesterson_corpus = ''


def count_and_prob(corpus, count, prob):
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

def get_links(): 

	austen_links = ["http://www.gutenberg.org/cache/epub/42671/pg42671.txt","http://www.gutenberg.org/cache/epub/42671/pg42671.txt",
	               "https://www.gutenberg.org/files/1212/1212-0.txt", "https://www.gutenberg.org/files/141/141-0.txt", 
	                "https://www.gutenberg.org/files/121/121-0.txt", "https://www.gutenberg.org/files/121/121-0.txt", 
	                "http://www.gutenberg.org/cache/epub/161/pg161.txt", "http://www.gutenberg.org/cache/epub/946/pg946.txt"]

	response = request.urlopen(url)

	austen_corpus = ""

	for link in austen_links: 
	    response = request.urlopen(link)
	    austen_corpus += response.read().decode('utf8')

	# austen_corpus[:100]

	# G.K. Chesterton
	chesterton_links = ["http://www.gutenberg.org/files/1717/1717-h/1717-h.htm", "http://www.gutenberg.org/files/11505/11505-h/11505-h.htm", 
	                   'http://www.gutenberg.org/cache/epub/1720/pg1720-images.html','http://www.gutenberg.org/files/20897/20897-h/20897-h.htm'
	                   'http://www.gutenberg.org/files/11339/11339-h/11339-h.htm', 'http://www.gutenberg.org/files/470/470-h/470-h.htm',
	                   'http://www.gutenberg.org/files/16769/16769-h/16769-h.htm','http://www.gutenberg.org/files/5265/5265-h/5265-h.htm']

	for link in chesterton_links: 
	    response = request.urlopen(link)
	    chesterton_corpus += response.read().decode('utf8')

	# Shakespeare
	# Complete works:
	shakespeare_links = ['http://www.gutenberg.org/files/100/100-h/100-h.htm']

	for link in shakespeare_links: 
	    response = request.urlopen(link)
	    shakespeare_corpus += response.read().decode('utf8')


	# Sir Arthur Conan Doyle
	doyle_links = ['http://www.gutenberg.org/files/1661/1661-h/1661-h.htm','http://www.gutenberg.org/files/2852/2852-h/2852-h.htm',
	              'http://www.gutenberg.org/files/244/244-h/244-h.htm', 'http://www.gutenberg.org/files/2097/2097-h/2097-h.htm',
	              'http://www.gutenberg.org/files/834/834-h/834-h.htm', 'http://www.gutenberg.org/files/108/108-h/108-h.htm', 
	              'http://www.gutenberg.org/files/2350/2350-h/2350-h.htm', 'http://www.gutenberg.org/files/537/537-h/537-h.htm']

	for link in doyle_links: 
	    response = request.urlopen(link)
	    doyle_corpus += response.read().decode('utf8')

	# Fyodor Doestevsky 
	doestevsky_links = ['http://www.gutenberg.org/files/28054/28054-h/28054-h.html', 'http://www.gutenberg.org/files/8578/8578-h/8578-h.htm', 
	                   'http://www.gutenberg.org/files/2638/2638-h/2638-h.htm', 'http://www.gutenberg.org/files/36034/36034-h/36034-h.htm',
	                   'https://www.gutenberg.org/files/2554/2554-h/2554-h.htm','http://www.gutenberg.org/files/2302/2302-h/2302-h.htm',
	                   'http://www.gutenberg.org/files/8117/8117-h/8117-h.htm']

	for link in doestevsky_links: 
	    response = request.urlopen(link)
	    doestevsky_corpus += response.read().decode('utf8')

