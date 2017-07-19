import sys
import math
import nltk
import math
import time
import itertools
import collections
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000

# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    SPLIT_CRITERIA = "/"
    brown_words = []
    brown_tags = []
    for sent in brown_train:
	tokens = sent.strip().split()
	words = [START_SYMBOL]+ [START_SYMBOL]+  [i.rsplit(SPLIT_CRITERIA,1)[0] for i in tokens] + [STOP_SYMBOL] #using start symbol twice as we nned it to compute trigrams
	tags =  [START_SYMBOL] + [START_SYMBOL] +  [j.rsplit(SPLIT_CRITERIA,1)[1] for j in tokens] + [STOP_SYMBOL] 
	brown_words.append(words)
	brown_tags.append(tags)
    return brown_words, brown_tags


# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    q_values = {}
    bg = []
    for lines in brown_tags:
	bigrams = [i for i in nltk.bigrams(lines)]
	bg.append(bigrams)
    bigram = list(itertools.chain(*bg))
    bigram_counter = collections.Counter(bigram) # Dictionary of bigram counts
    
    b = []
    for lines in brown_tags:
	trigrams = [i for i in  nltk.trigrams(lines)]
	b.append(trigrams)
    trigram = list(itertools.chain(*b))
    bigram_counter[(START_SYMBOL, START_SYMBOL)] = len(brown_tags) # Set count of twice start symbol to number of sent to avoid key error
    trigram_counter = collections.Counter(trigram)
    total_trigram = sum(trigram_counter.itervalues())
    q_values = {k: math.log(float(v) / bigram_counter[k[:2]],2) for k, v in trigram_counter.iteritems()} # dictionary of the for (word,tag) : prob
    return q_values
# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()

# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    all_words = list(itertools.chain(*brown_words))
    counter = collections.Counter(all_words)
    p1 = { key:value for key, value in counter.items() if value > 5 }
    known_words = p1.keys() # Keys of dictionary return a unique set
    return known_words
# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    
    brown_words_rare = brown_words
   
    for i,lis in enumerate(brown_words_rare):
	for j,word in enumerate(lis):
		if word not in known_words:
			brown_words_rare[i][j] = "_RARE_"
	
    return brown_words_rare
# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()

# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):      
    e_values = {}
    word_count = collections.defaultdict(int)
    tags_count = collections.defaultdict(int)
    for wordlist, taglist in zip(brown_words_rare, brown_tags):
        for word, tag in zip(wordlist, taglist):
            word_count[(word, tag)] += 1
            tags_count[tag] += 1
    for (word, tag),value in word_count.iteritems():
        e_values[(word, tag)] = math.log(float(value) / tags_count[tag], 2) # p(a/b) = p(a  and b)/p(b)
   
    return e_values , tags_count.keys()
# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()

# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words,taglist,known_words,q_values,e_values):
    
    tagged = []
    def get_tags(k,taglist): # Function to get the right tag (from taglist or default value)
   	 if k < 0:
       	     a =  [START_SYMBOL]
   	 else:
             a = taglist
         return a        
    for lines in brown_dev_words:
	    vmax = " "
            umax = " "
	    n = len(lines)
	    tag_line = [None]*n
	    viterbi_vals = {} # viterbi score values
	    bp = {} # Memoization step
	    viterbi_vals[-1,START_SYMBOL,START_SYMBOL] = 0 #prob of a word before two start symbols is assumed to be zero
	    
	    for k in range(0,n):
		token = lines[k]
		if token not in known_words:
		    token = RARE_SYMBOL
		for (u, v) in itertools.product(get_tags(k-1,taglist),get_tags(k,taglist)):
	
			if e_values.get((token,v),) is not None:#Do not consider tokens with emission prob zero 
			    
				viterbi_max = -float("inf")
				tag_viterbi_max = ""
				for w in get_tags(k-2,taglist):
				    vit_score = viterbi_vals.get((k-1,w,u),-float("inf")) + q_values.get((w,u,v),LOG_PROB_OF_ZERO) + e_values[token,v]
				    if(vit_score > viterbi_max):
					viterbi_max = vit_score
					tag_viterbi_max = w
				viterbi_vals[k,u,v] = viterbi_max
				bp[k,u,v] = tag_viterbi_max
            vit_max = -float("inf")
            for (v,u) in itertools.product(get_tags(n-1,taglist),get_tags(n-2,taglist)):  #this is to calculate viterbi score and update backpointer for last 2 vals of algorithm 
		    vit_score = viterbi_vals.get((n-1,u,v),-float("inf")) + q_values.get((u,v,STOP_SYMBOL), LOG_PROB_OF_ZERO)
		    if vit_score > vit_max:
			vmax = v
			umax = u
            tag_line[n-2:n] = umax,vmax
	    for k in xrange(n-3,-1,-1):
		tag_line[k] = bp[k+2,tag_line[k+1],tag_line[k+2]]  # Backtrace the backpointer to get sentence in the right order
            
            tag_line = " ".join(i + "/" + j for (i,j) in zip(lines,tag_line)) + "\n"
       	    tagged.append(tag_line)
    return tagged
    
 
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]
    # IMPLEMENT THE REST OF THE FUNCTION HERE
    tagged = []
    NLTK_default_tagger = nltk.DefaultTagger('NOUN') # create the default tagger
    bigram_tagger = nltk.BigramTagger(training, backoff= NLTK_default_tagger) # use default tagger as a backoff in bigram tagger
    trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger) # use bigram tagger as default in tri gram tagger
    
    for lines in brown_dev_words:
	a= " ".join([token + "/" + tag for token,tag in trigram_tagger.tag(lines)]) + "\n"
        tagged.append(a)
    return tagged
# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()
DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'
def main():
    # start timer
    time.clock()
    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()
    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)
    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)
    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')
    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)
    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)
    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")
    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)
    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")
    # delete unneceessary data
    del brown_train
    del brown_words_rare
    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()
    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])
    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)
    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')
    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)
    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')
    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'
if __name__ == "__main__": main() 
