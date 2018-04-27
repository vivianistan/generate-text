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

* `def count_and_prob_bigram(corpus, count, prob)`: returns the count and probabilities of words

* `def gen_next_word(word, prob_dict)`: generates a word given a previous word and a probability dictionary

## Markov Chains
I used [this](https://towardsdatascience.com/simulating-text-with-markov-chains-in-python-1a27e6d13fc6) site as reference.

I implemented a very simple Markov chain to generate text. First I generated pairs of words for the text, then I went through all the word pairs and used a dictionary to store all the words that occur after a chosen word. To generate a next word given a current word, I randomly pick a word from the next word list of the current word. A visual depiction of what this process might look like is shown below. Overall, the theory for this method also sounds very similar to the bigram implementations, but variation in the implementation may affect results.

![GUI Interface](https://github.com/vivianistan/generate-text/blob/master/docs/Pics/markov-trump-graph.png "Markov Chain text generation example")



## Mixing texts
To mix texts I simply generated a random number for each word and compared it to the user inputted ratio. 

## Evaluation Metrics
To evaluate the different text generation methods, I surveyed some people and asked them to rate the generated text from 1-10 based on how well the generated text matched the overall style of the original author. 


# Results

For generating text from one author, the ratings had a lot of variance, and each of the techniques ended up getting the same average score: 5.6 out of 10. The results can be seen in the figure below. This indicates that each technique performs similarly generating texts from one author, however since I only surveyed 10 people and the data has a lot of variance, the results could change if I poll more people.

![GUI Interface](https://github.com/vivianistan/generate-text/blob/master/docs/Pics/graph1.png "Survey results for generating text from one author")

For generating text from two different authors, the scores were on average lower than the scores for generating text from one author only with averages of 4.2 for NLTK-2gram, 4.3 for Custom-2gram, and 3.7 for Markov Chains. These scores indicate that the Custom-2gram is slightly better than NLTK-2gram at mixing different author styles and both 2grams are better than Markov Chains at mixing styles.

![GUI Interface](https://github.com/vivianistan/generate-text/blob/master/docs/Pics/graph2.png "Survey results for generating text from two authors")

Interestingly, overall, people rated Markov Chains as the best, followed by the Custom-2gram, with the NLTK-2gram last. This tells me that Markov Chains produce the most cohesive randomly generated text but is bad at mixing them and/or that it’s simply quite difficult to quantitatively assess or distinguish the quality of the random text generation techniques I chose. Given that the theory behind each technique is quite similar, I’m more inclined to believe the latter.


![GUI Interface](https://github.com/vivianistan/generate-text/blob/master/docs/Pics/graph3.png "Survey results for overall technique quality")


# Getting Started
## Running the application
You will have to modify the `path` names in `generate.py` in the `get_text_local(complete_corpus)` method. 

Then you can run:

`python3 generate_text_gui.py`
