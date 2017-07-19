from nltk.corpus import comtrans
import A
import B
import C

import time 

tick1 = time.time()
if __name__ == '__main__':
    aligned_sents = comtrans.aligned_sents()[:350]
    A.main(aligned_sents)
    B.main(aligned_sents)
tick2 = time.time()

print tick2-tick1
