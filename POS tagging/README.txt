Unique name : anuragb  Name: Anurag Beniwal

A1 
UNIGRAM natural -13.766408817
BIGRAM natural that -4.05889368905
TRIGRAM natural that he -1.58496250072

A2
Perplexity: 
Unigram model -  1052.4865859
Bigram model -  53.8984761198
Trigram model - 5.7106793082

A3
Linear interpolated model perplexity -  12.9590272322

A4
The perplexity is lower for the trigram model than the linear interpolated model . The reason for this is that the weights in the interpolated model are considered equal and not learnt by max liklihood . We know that in general trigram model is better but still we end up giving equal weights to uni, bi and tri gram models . If the weights are estimated using max. liklihood the interpolated model might end up having a lower perplexity than trigram.

A5
Perplexity of “Sample1_scored.txt” is 1.55575702577
Perplexity of “Sample2_scored.txt” is 2.56578048202e+26

As we see that the perplexity of second sample is incredibly higher than the first . This means that the first score "Sample1_Scored.txt" is from Brown corpus.
Perplexity is used to evaluate effectiveness of language models and lower the perplexity (proportional to entropy) the better a langauge model is .
Now since the perplexity for scores based on sample 1 on brown corpus is lower which means tht the model was trained ona dataset similar/equivalent to brown corpus.


B2

TRIGRAM CONJ ADV ADP -2.9755173148
TRIGRAM DET NOUN NUM -8.9700526163
TRIGRAM NOUN PRT PRON -11.0854724592


B4
** - 0
Night NOUN -13.8819025994
Place VERB -15.4538814891
prime ADJ -10.6948327183
STOP STOP 0.0
_RARE_ VERB -3.17732085089

B5

Accuracy : 91.75%


B6
Percent correct tags: 87.9985146677


Time taken
solutionsA.py : 13.31 seconds
solutionsB.py : 225 seconds

