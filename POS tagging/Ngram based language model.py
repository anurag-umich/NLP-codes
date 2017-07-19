import math
import nltk
import time
import itertools
import collections


# Constants to be used by you when you fill the functions
START_SYMBOL = "*"
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000


# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):
    unigram_p = {}
    bigram_p = {}
    trigram_p = {}
    unicounter = {}
    u = []
    for sent in training_corpus:
	a = sent.strip().split() + [STOP_SYMBOL]
	u.append(a)
    unigram =[(i,) for i in  list(itertools.chain(*u))]
    unigram_counter = collections.Counter(unigram) # count all unigrams
    total = sum(unigram_counter.itervalues(), 0.0) # sum of all unigrams
    unigram_p = {k: math.log(float(v) / total,2) for k, v in unigram_counter.iteritems()} #unigram probability
	
    b =[]
    for sent in training_corpus:
        tokens = sent.strip().split()

	tokens1 = [START_SYMBOL] + tokens + [STOP_SYMBOL] # Add start and stop to bigram
  	bigrams = [i for i in  nltk.bigrams(tokens1)]
	b.append(bigrams)
  

    bigram = list(itertools.chain(*b))
    bigram_counter = collections.Counter(bigram)
    total_bigram = sum(bigram_counter.itervalues(), 0.0)
    unigram_counter[(START_SYMBOL,)] = len(training_corpus) # add start symbol count to unigram counter
    unigram_counter[(STOP_SYMBOL,)] =len(training_corpus) 
    
    bigram_p = {k: math.log(float(v)/float(unigram_counter[(k[0],)]),2) for k, v in bigram_counter.iteritems() } #p(A/B) = P(A and B)/P(B)
    #bigram_p = {k : unigram_counter[k[0]] for k,v in bigram_counter.iteritems()}
    b =[]
    for sent in training_corpus:
	tokens = sent.strip().split()
	tokens1 = [START_SYMBOL] + [START_SYMBOL] + tokens + [STOP_SYMBOL] #Add two start symbols to trigram and a stop symbols
  	trigrams = [i for i in  nltk.trigrams(tokens1)]
	b.append(trigrams)

    trigram = list(itertools.chain(*b))
    trigram_counter = collections.Counter(trigram)
    bigram_counter[(START_SYMBOL,START_SYMBOL)] = len(training_corpus)
    total_trigram = sum(trigram_counter.itervalues(), 0.0)
    trigram_p = {k:math.log(float(v) /bigram_counter[k[:2]] ,2) for k, v in trigram_counter.iteritems()} # p(A/B,C) = P(A and B and C)/P(C)
    return unigram_p, bigram_p, trigram_p


# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()



# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    scores = []
    for line in corpus:
	log_score = 0
    	a =line.strip().split()
	if n ==1:
	   token = a + [STOP_SYMBOL]
	   ngrams  = [(i,) for i in token]
	   
	elif n==2:
           ngrams = nltk.bigrams([START_SYMBOL] + a + [STOP_SYMBOL])
        elif n ==3:
	   ngrams  = nltk.trigrams([START_SYMBOL]+ [START_SYMBOL]  + a + [STOP_SYMBOL])
        
	
        for grams in ngrams:
		try:
	           log_prob = ngram_p[grams]
		   log_score = log_score + log_prob
	        except KeyError: # Set the log score of each sentence to -1000 in case of a key error
		   logscore = MINUS_INFINITY_SENTENCE_LOG_PROB   
                
	           
                
        scores.append(log_score)
	   
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()


# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []
    lambda_wt = float(1)/3 #weight for interpolation
    START_SYMBOL = "*"
    STOP_SYMBOL = "STOP"
    for lines in corpus:
	log_score = 0
	token =[START_SYMBOL] + [START_SYMBOL] +  lines.strip().split() +[STOP_SYMBOL]
	for triplet in nltk.trigrams(token):
	
		try:
			tri = trigrams[triplet]
		except KeyError: # replace prob by -1000 in case key is not found
			tri = MINUS_INFINITY_SENTENCE_LOG_PROB
                try:
			bi = bigrams[triplet[1:3]]
                except KeyError:
			bi = MINUS_INFINITY_SENTENCE_LOG_PROB
                try:
			uni = unigrams[triplet[2]]
                except KeyError:
			uni =  MINUS_INFINITY_SENTENCE_LOG_PROB
		log_score += math.log(lambda_wt* (2 ** tri) + lambda_wt * (2 ** bi) + lambda_wt * (2 ** uni), 2) # formula for linear interpolation with const weight
	scores.append(log_score)
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'


def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
