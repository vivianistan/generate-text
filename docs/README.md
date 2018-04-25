# Generate Text - Experimenting with different styles

> A random text generation GUI

Final project for LIN 353C (Intro to Computational Linguistics)

* [Site](https://vivianistan.github.io/generate-text/#/)
* [Code](https://github.com/vivianistan/generate-text)


![GUI Interface](https://github.com/vivianistan/generate-text/blob/master/docs/Pics/gui.png "GUI Interface")


# Background
This application can generate random text in the style of 5 different authors using some of their works from [Project Gutenberg](http://www.gutenberg.org): 
* Jane Austen
* G.K. Chesterton
* William Shakespeare
* Sir Arthur Conan Doyle
* Fyodor Dostoyevsky

The application can also mix styles of two different authors on a variable ratio.

It generates text using bigrams with Maximum Likelihood Estimation (MLE) and Markov Chains.

The GUI was made using PyQT5 in Python3

# Approach

## Preprocessing
Originally, I was going to compile corpuses for each other by reading from urls to plain text files, but this took too long. So I downloaded up to 7 works from Project Gutenberg for each author in plain text file format then processed them minimally using regular expressions (regex). This preproccessing step takes a while, usually around 45s. 


## Bigrams
I two methods for generating text with bigrams: one primarily using built-in NLTK functions and the other was by hand. 

### NLTK

I used NLTK to get the bigrams for each corpus, get a conditional frequency distribution, conditional probability distribution, and generate words based off of that model.

Here are the code snippets where you can see this:

`cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(tokens))`
`cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.MLEProbDist)`
...
`word = cprob_gram2[word].generate()`

### Custom bigram
I just used this formula to calculate the conditional probabilities:

P(word2|word1) = count(word1, word2)/count(word1, ...)

Here are the methods I wrote:

`def count_and_prob_bigram(corpus, count, prob)`: returns the count and probabilities of words
`def gen_next_word(word, prob_dict)`: generates a word given a previous word and a probability dictionary

## Markov Chains
I used [this](https://towardsdatascience.com/simulating-text-with-markov-chains-in-python-1a27e6d13fc6) site as reference.

## Mixing texts
To mix texts I simply generated a random number for each word and compared it to the user inputted ratio. 

## Evaluation Metrics
To evaluate the different text generation methods, I surveyed some people on which they thought was best.

# Results

# Getting Started
## Running the application
You will have to modify the `path` names in `generate.py` in the `get_text_local(complete_corpus)` method 

`python3 generate_text_gui.py`
