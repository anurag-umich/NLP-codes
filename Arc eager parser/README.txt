1) Dependency graph

partb)
The method to visually find if a sentence has a projective or non projective dependence graph is to check if the two arcs cross each other in the graph. If the arcs cross each other its a non-projective dependency tree and vice versa .
In the code provided , we see the same logic implemented

Steps:
For each node in the dependency graph , if the node has head then the child node is the node itself and the parent node is with the address of head
Now the index of child node could be less than or greater than the parent node. Just for the ease of writing a program we get all child nodes on left of parent node
and apply the following rule :
For all nodes between child and parent node if the arcs originating from them or ending at them come from/go to a node that is outside the (child node -parent node) range then it isnot a projective node. This is exactly the same logic as of crossing of two arcs .


partc)

English Projective : $ 500 million of Remic mortgage securities offered in 13 classes by Prudential-Bache Securities Inc.

English Non projective :John saw a dog yesterday which was a Yorkshire Terrier 

2) Manipulating configurations

partb)

UAS: 0.229038040231 
LAS: 0.125473013344


partc)
The LAS value is pretty low for badfeatures.model as it doesn't have sufficient number of features. We see later that the performance significantly increases when we increase the number of features.

3)

Featureextractor
Part a)
The ideas of these features were borrowed from paper called  Transition-based Dependency Parsing with Rich Non-local Features by Nivre and Zhang

1) Part of speech tags of Stack[-1] and buffer[0] : These features are the most effective features among all , they lead to more than 50% increase in the LAS as well as UAS 
   This is only true when we use them as unigram features . When we create bi gram and trigram features of Stack-Buffer POS tags we find that the accuracy decreases significantly .
   The reason for this could be the small size of training data (200 lines) . Trigram and bigram features would overfit over such a small dataset .If we use tags from tagged data directly , then the complexity of this feature is O(n) in time .

2) Word form features : these features are resonably good and give 12% increase in LAS as compared to bad features model 


3) Another interesting feature that I tried was distance between a pair of head and modifier . However this feature lead to marginal increase in LAS (about 1%). The complexity of this feature is also O(n square) in the worst case .


4) I also tried left dependency and right dependency features . These features increase the accuracy marginally . 

5) Valency : we use number of modifiers to a given head also as a feature . This feature has feature complexity of O(n square).

6) Lemma : We use lemma of the stock[-1] and buffer[0] and we observe that using lemma of just buffer increases accuracy by about 1% but using lemma of stock[-1] decreases LAS slightly.

7) Address : This is a bad feature as in all models it decreases the LAS and UAS considerably. Here also the reason could be overfitting as we train this on just 200 sentences and address could be a very sparse feature in this scenario. The feature complexity is O(n) for this feature.

8) Universal tag : we use universal tag as a feature and it leads to slight increase in accuracy for all three models . This also has a time complexity of O(n) for a sentence.


We see that these features work best in case of English , followed by Danish . They do not work very well for Swedish.

Partb)

Performance of Swedish parser :
UAS: 0.793865763792 
LAS: 0.681537542322


Performance of Danish Parser:
UAS: 0.804790419162 
LAS: 0.719161676647


Performance of English parser:

UAS :0.87 
LAS: 0.78


Partc)

Complexity of Arc eager shift reduce parser:

In the transition parser script, we see that the static version of arc eager parser is being implemented .this parser is linear in n (number of tokens in the sentence).
The trade offs that this parser makes include :
The static nature of parser makes it chose just one sequence out of the possible many for a given gold tree . This could lead to sub optimal sequences.When the parser doesn't find a canonical sequence exactly like that in the gold tree it throws an error and this could be fixed using the dynamic version of the parser.
Another tradeoff that we make is we loose some data (more in few languages like swedish and less in English) due to non projective dependency graphs .
This parser cannot handle non projective dependency trees. However, this is very fast in terms of time and space complexity as compared to other parsers due to its deterministic nature .



