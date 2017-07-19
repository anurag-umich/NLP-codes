import nltk
from nltk.corpus import comtrans
from nltk.align import IBMModel1,IBMModel2
from nltk.align import AlignedSent, Alignment
import C
# Initialize IBM Model 1
def create_ibm1(aligned_sents):
    Ibm1 = IBMModel1(aligned_sents, 10)
    return Ibm1 

# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    Ibm2 = IBMModel2(aligned_sents,10)
    return Ibm2



def compute_avg_aer(aligned_sents, model, n):
    sum_aer = float(0)
    for i in range(0,n):
	ali  = model.align(aligned_sents[i])
        sum_aer = sum_aer + float(ali.alignment_error_rate(aligned_sents[i]))
    avg_aer = sum_aer/float(n)
    return avg_aer

# Computes the alignments for the first 20 sentences in
# aligned_sents and saves the sentences and their alignments
#  to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
    f = open(file_name, 'w') 

    for i in range(0,20):
	ali  = model.align(aligned_sents[i])
        f.write("%s\n" % ali.mots)
        f.write("%s\n" % ali.words)
        f.write("%s\n" % ali.alignment)
        f.write('\n')
    f.close()
    return

def save_model_output1(aligned_sents, model1,model2,model3, file_name):
    f = open(file_name, 'w')

    for i in range(0,20):
        ali_ibm1  = model1.align(aligned_sents[i])
        ali_ibm2 = model2.align(aligned_sents[i])
        ali_berkeley = model3.align(aligned_sents[i])
        f.write("%s\n" % ali_ibm1.mots)
        f.write("%s\n" % ali_ibm1.words)
        f.write("%s\n" % ali_ibm1.alignment)
        f.write("%s\n" % ali_ibm1.alignment_error_rate(aligned_sents[i]))
        f.write("%s\n" % ali_ibm2.alignment_error_rate(aligned_sents[i]))
        f.write("s\n" % ali_berkeley.alignment_error_rate(aligned_sents[i]))
        f.write('\n')
    f.close()
    return
    	
    

def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    #save_model_output1(aligned_sents,ibm1,ibm2,"ibm1_ibm2_err.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)
    #berkeley = BerkeleyAligner(aligned_sents,10)
    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    #save_model_output1(aligned_sents,ibm1,ibm2,berkeley,"ibm1_ibm2_berk_err.txt")
    #save_model_output1(aligned_sents,ibm2,"ibm2_aer.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
