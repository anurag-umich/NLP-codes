
PART A
###compute AER of IBM model 1 and 2 ############

IBM Model 1: <= 0.665 IBM Model 2: <= 0.650

################### Sentences when 1 model outperforms other ####################

For sentence 5
[u'Please', u'rise', u',', u'then', u',', u'for', u'this', u'minute', u"'", u's', u'silence', u'.']
[u'Ich', u'bitte', u'Sie', u',', u'sich', u'zu', u'einer', u'Schweigeminute', u'zu', u'erheben', u'.']

AER IBM Model1 = 0.75
AER IBM Model2 = 0.666666666667

For this sentence IBM2 outperforms IBM1
In most of the sentences IBM2 tends to perform better than IBM2 as the probabilities of distortion and translation following a uniform distribution as assumed in IBM 1 is very unlikely and may lead to biased calculation of the quasi liklihood function.The counts in turn (if the corpus is big enough ) can be more helpful in caculating a true liklihood .


Sentence 8 :
[u'You', u'will', u'be', u'aware', u'from', u'the', u'press', u'and', u'television', u'that', u'there', u'have', u'been', u'a', u'number', u'of', u'bomb', u'explosions', u'and', u'killings', u'in', u'Sri', u'Lanka', u'.']
[u'Wie', u'Sie', u'sicher', u'aus', u'der', u'Presse', u'und', u'dem', u'Fernsehen', u'wissen', u',', u'gab', u'es', u'in', u'Sri', u'Lanka', u'mehrere', u'Bombenexplosionen', u'mit', u'zahlreichen', u'Toten', u'.']

AER IBM model1 :0.791666666667
AER IBM Model2 :0.833333333333

For this sentence IBM1 outperforms IBM2
One possible reason for IBM1 performing better than IBM2 is that the counts of c(f,e) for certain words may not have enough occurances in the corpus and which my lead to biased estimate of the probability t(f/e) and t(e/f) . In such situations the estimate of t(f/e) and other probability calculated based on uniform distribution may be a better estimate as compared to the counts . This leads to a better AER for ibm1 than ibm2 .


IBM model 1 :
n_iter, AER, Time
2 , 0.684, 5.93
4, 0.63 , 11.562
6, 0.626 , 17.002
8, 0.631 , 22.576
10 , 0.665 , 28.95
12, 0.666 , 33.6
14, 0.665 , 39.22
16 , 0.665, 44.67
18 , 0.661 ,49.87
20 , 0.661 ,56.93
30 , 0.660 ,83.86

From the data above we can see that from 2-6 iteration the average AER decreases and then starts increasing ( this may be a local minima) The AER increases to 0.665 and stays about the same till iteration 16 and then slightly decreases to 0.661 . We see that at n_iter = 30 also the AER is more or less similar. Therefore, It is safe to assume the EM converges at 18 iterations.
As we see the time almost doubles for the first few iterations and then increases slowly than before .

We see that inititally the AER is lower than when we iterate more because inittially the quasiliklihood is far away from the true liklihood and the alignment we get is by maximizing the quasi liklihood instead of real liklihood which may be misleading.However, as we iterate more and more the quasi liklihood moves closser to real liklihood and maximizing this quasi liklihood then may give us the true maximum.

IBM Model2 :
n_iter , AER, time
2, 0.644 ,37.20
4,0.642,52.2774438858
6, 0.647,66.95
8,0.649,85
10,0.650,90.14
14,  0.652,112
18, 0.651,149
25 ,0.649, 180
30 ,0.649, 260

The algorithm average AER first decreases with n_iter upto 10 and then becomes more or less constant. The global minimum lies at about 20 iterations. However , the time complexity increases fast so there is not much gain in proceeding after 10 iteratioins. Time complexity of IBMmodel is higher than IBM1 as it requires more computation of counts for updates unlike IBM where the updates are constant.


Part B:

Overall Berkeley aligner works better than both IBM model 1 and IBM model2 with average AER of 0.547 as compared to 0665 and 0.65 of IBM model 1 and 2 respectively. The model works well as it removes any directional bias in calculation of counts by averaging the counts .

[u'Resumption', u'of', u'the', u'session']
[u'Wiederaufnahme', u'der', u'Sitzungsperiode']
0-0 1-1 1-2 2-3
0.0

The berkeley aligner outperforms both IBM model 1 and model2 for first sentence as it has a perfect accuracy for this sentence. The averaging of counts helps in this particular sentence which leads to better accuracy than IBM model1 and 2










