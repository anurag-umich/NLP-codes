import nltk
import A
from collections import defaultdict

from nltk.align import Alignment
from nltk.align import AlignedSent
class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.probabilities, self.alignments = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
       # probabilities, alignments = train(aligned_sents,num_iter)
        alignment = []
        l_e = len(align_sent.words)
        l_f = len(align_sent.mots)
        eng_words = align_sent.words
        french_words = align_sent.mots
        for i,mot in enumerate(french_words):
            # Initialize the maximum probability with - infinity
            max_align_prob = -float("inf")
            for j,word  in enumerate(eng_words): 
                prob =  self.probabilities[(mot,word)]*self.alignments[(j,i,l_e,l_f)]
                if prob >= max_align_prob:
                   max_align_prob = prob
                   best_align = j
            
            alignment.append((best_align, i))
    #conver the alignment list to Alignment object
        alignment = Alignment(alignment)
        return AlignedSent(align_sent.words, align_sent.mots, alignment)  
    
    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iter):
       #c_fe = defaultdict(lambda: 0.0)
       #c_ef = defaultdict(lambda: 0.0)
       #c_e = defaultdict(lambda: 0.0)
       #c_f = defaultdict(lambda: 0.0)
       #c_q_fe = defaultdict(lambda: 0.0)
       #c_q_ef = defaultdict(lambda: 0.0)
       #c_q_fe_total = defaultdict(lambda: 0.0)
       #c_q_ef_total = defaultdict(lambda: 0.0)
       #sum_q_fe = defaultdict(lambda: 0.0)
       #eng_vocab = set()
       #french_vocab = set()

        n_e = defaultdict(lambda: 0.0)
        for sent in aligned_sents:
            for e in sent.words:
                n_e[e] = n_e[e] + len(sent.mots)
        n_f = defaultdict(lambda: 0.0)        
        for sent in aligned_sents:
            for f in sent.mots:
                n_f[f] = n_f[f] + len(sent.words)
        t_fe = defaultdict(lambda: 0.0)
        t_ef = defaultdict(lambda: 0.0)
        q_fe = defaultdict(lambda: 0.0)
        q_ef = defaultdict(lambda: 0.0)
        for sent in aligned_sents:
            for f in sent.mots:
 		for e in sent.words:
	            t_fe[(f,e)] = 1.0/float(n_e[e])
                    t_ef[(e,f)] = 1.0/float(n_f[f])
            m = len(sent.mots)
            l = len(sent.words)
            for i in range(0,m):
           	for j in range(0,l):
		    q_fe[(j,i,l,m)] = 1.0/float(l+1)
                    q_ef[(i,j,m,l)] = 1.0/float(m+1)
	for n in range(0,num_iter):
	    c_fe = defaultdict(lambda: 0.0)
            c_ef = defaultdict(lambda: 0.0)
            c_e = defaultdict(lambda: 0.0)
            c_f = defaultdict(lambda: 0.0)
            c_q_fe = defaultdict(lambda: 0.0)
            c_q_ef = defaultdict(lambda: 0.0)
            c_q_fe_total = defaultdict(lambda: 0.0)
            c_q_ef_total = defaultdict(lambda: 0.0)
            #sum_q_fe = defaultdict(lambda: 0.0)
            eng_vocab = set()
            french_vocab = set()
            r = []
            for sent in aligned_sents:
                eng_vocab.update(sent.words)
                french_vocab.update(sent.mots)
                q_fe_list = []
                q_ef_list = []
                #sum_q_fe = defaultdict(lambda: 0.0)
                #sum_q_ef = defaultdict(lambda: 0.0)
                eng_words = sent.words
                french_words = sent.mots
                m = len(sent.mots)
                l =  len(sent.words)
                for i in range(0,m):
                    for j in range(0,l):
                        sigma_delta1 = 0.0
                        sigma_delta2 = 0.0
                        for h in range(l):
                            sigma_delta1 = sigma_delta1 + q_fe[(h,i,l,m)]*t_fe[(french_words[i],eng_words[h])]
                            sigma_delta2 = sigma_delta2 + q_ef[(i,h,m,l)]*t_ef[(eng_words[h],french_words[i])]
                    #sum_q_fe[i]= sum(q_fe_list)
                    #sum_q_ef[i] = sum(q_ef_list)
                
                    
                        delta1 = q_fe[(j,i,l,m)]*t_fe[(french_words[i],eng_words[j])]/ float(sigma_delta1)
                        delta2 = q_ef[(i,j,m,l)]*t_ef[(eng_words[j],french_words[i])]/ float(sigma_delta2)
                        delta = float(delta1+delta2)/2
                        c_fe[(french_words[i],eng_words[j])] += delta
                        c_ef[(eng_words[j],french_words[i])] += delta
                        c_e[eng_words[j]] += delta
                        c_f[french_words[i]] +=delta
                        c_q_fe[(j,i,l,m)] += delta
                        c_q_ef[(i,j,m,l)] +=delta
                        c_q_fe_total[(i,l,m)] += delta
                        c_q_ef_total[(j,m,l)] += delta
           # for  key in c_fe.keys():
                # c_fe[key] = (c_fe[key] + c_ef[reversed(key)])/2 
                # c_ef[tuple(reversed(key))] = c_fe[key]
           # for sent in aligned_sents:
               # eng_words = sent.words
               # french_words = sent.mots
               # m = len(sent.mots)
               # l = len(sent.words)
               # for i in range(0,m):
                   # for j in range(0,l):
                       # c_q_fe[(j,i,l,m)] = (c_q_fe[(j,i,l,m)] + c_q_ef[(i,j,m,l)])/2
                       # c_q_ef[(i,j,m,l)] = c_q_fe[(j,i,l,m)]
            
           # for key in c_fe.keys():
               # t_fe[key]    =  c_fe[key]/c_e[key[1]]
               # t_ef[tuple(reversed(key))] = c_ef[tuple(reversed(key))]/c_f[key[0]]

            for sent in aligned_sents:
                eng_words = sent.words
                french_words = sent.mots
                m = len(sent.mots)
                l = len(sent.words)
                for i in range(0,m):
                    for j in range(0,l):
                        t_fe[(french_words[i],eng_words[j])] = c_fe[(french_words[i],eng_words[j])]/c_e[eng_words[j]]
                        t_ef[(eng_words[j],french_words[i])] = c_ef[(eng_words[j],french_words[i])]/c_f[french_words[i]]
                        q_fe[(j,i,l,m)] = c_q_fe[(j,i,l,m)]/c_q_fe_total[(i,l,m)]
                        q_ef[(i,j,m,l)] = c_q_ef[(i,j,m,l)]/c_q_ef_total[(j,m,l)]
          
        return t_fe ,q_fe

def save_model_output1(aligned_sents, model1, file_name):
    f = open(file_name, 'w')

    for i in range(0,20):
        ali_ibm1  = model1.align(aligned_sents[i])
        #ali_ibm2 = model2.align(aligned_sents[i])
        #ali_berkeley = model3.align(aligned_sents[i])
        f.write("%s\n" % ali_ibm1.mots)
        f.write("%s\n" % ali_ibm1.words)
        f.write("%s\n" % ali_ibm1.alignment)
        f.write("%s\n" % ali_ibm1.alignment_error_rate(aligned_sents[i]))
        #f.write("%s\n" % ali_ibm2.alignment_error_rate(aligned_sents[i]))
       # f.write("s\n" % ali_berkeley.alignment_error_rate(aligned_sents[i]))
        f.write('\n')
    f.close()
    return            
        

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)
    #save_model_output1(aligned_sents,ba,"bekeley.txt")
    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
