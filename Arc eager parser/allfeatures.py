from nltk.compat import python_2_unicode_compatible

printed = False

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most
    
    @staticmethod
    def valency(idx, arcs):
        right_count = 0
        left_count = 0 
        for(wi,r,wj) in arcs:
            if (wi == idx and wj > wi) :
		right_count += 1
            if (wi == idx and wj < wi):
                left_count += 1
        return left_count , right_count

    @staticmethod
    def condition_check(n_stack,n_buffer,attr_stack,attr_buff):
       a = (len(stack) > n_stack -1)  and (len(buffer) >  n_buffer -1)
       b = False not in  [i in token_stack for i in attr_stack]
       c = False not in  [i in token_buffer for i in attr_buff]
       d = False not in[FeatureExtractor._check_informative(token_stack[i]) for i in attr_stack]
       e = False not in[FeatureExtractor._check_informative(token_buffer[i]) for i in attr_buff]
       return a and b and c and d and e
      

       
       
		
    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            print("This is not a very good feature extractor!")
            printed = True

        # features on top element of stack in a particular config
        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)
            if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
		result.append('STK_0_TAG_' + token['tag'])
            if 'address' in token and FeatureExtractor._check_informative(token['address']):
		result.append('STK_0_ADD_' + str(token['address']))           
            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)
            left_count, right_count = FeatureExtractor.valency(stack_idx0, arcs)
           
            if FeatureExtractor._check_informative(left_count):
               result.append('STK_0_LVAL_' + str(left_count))
            if FeatureExtractor._check_informative(right_count):
               result.append('STK_0_RVAL_' + str(right_count))
            
            if FeatureExtractor._check_informative(dep_left_most):
               result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
               result.append('STK_0_RDEP_' + dep_right_most)
        
        # features on second element of stack from top
	if len(stack) > 1:
		stack_idx1 = stack[-2]
		token = tokens[stack_idx1]
                if FeatureExtractor._check_informative(token['word'], True):
                   result.append('STK_1_FORM_' + token['word'])
                if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                   feats = token['feats'].split("|")
               	   for feat in feats:
                       result.append('STK_1_FEATS_' + feat)
                if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
               	   result.append('STK_1_TAG_' + token['tag'])
                if 'address' in token and FeatureExtractor._check_informative(token['address']):
               	   result.append('STK_1_ADD_' + str(token['address']))

                dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx1, arcs)
                left_count, right_count = FeatureExtractor.valency(stack_idx1, arcs)
        
                if FeatureExtractor._check_informative(left_count):
                   result.append('STK_1_LVAL_' + str(left_count))
                if FeatureExtractor._check_informative(right_count):
                   result.append('STK_1_RVAL_' + str(right_count))
           	if FeatureExtractor._check_informative(dep_left_most):
                   result.append('STK_1_LDEP_' + dep_left_most)
                if FeatureExtractor._check_informative(dep_right_most):
               	   result.append('STK_1_RDEP_' + dep_right_most)
        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)
            if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
		result.append('BUF_0_TAG_' + token['tag'])
            if 'address' in token and FeatureExtractor._check_informative(token['address']):
                result.append('BUF_0_ADD_' + str(token['address']))
            left_count, right_count = FeatureExtractor.valency(buffer_idx0, arcs)
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)
            
            if FeatureExtractor._check_informative(left_count):
               result.append('BUF_0_LVAL_' + str(left_count))
            if FeatureExtractor._check_informative(right_count):
               result.append('BUF_0_RVAL_' + str(right_count))
            if FeatureExtractor._check_informative(dep_left_most):
               result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
               result.append('BUF_0_RDEP_' + dep_right_most)
	
        if len(buffer) > 1 :
	    buffer_idx1 = buffer[1]
	    token = tokens[buffer_idx1]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_1_FORM_' + token['word'])
	    if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_1_FEATS_' + feat)
            if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                result.append('BUF_1_TAG_' + token['tag'])

            if 'address' in token and FeatureExtractor._check_informative(token['address']):
                result.append('BUF_1_ADD_' + str(token['address']))
            left_count, right_count = FeatureExtractor.valency(buffer_idx1, arcs)
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx1, arcs)

            if FeatureExtractor._check_informative(left_count):
               result.append('BUF_1_LVAL_' + str(left_count))
            if FeatureExtractor._check_informative(right_count):
               result.append('BUF_1_RVAL_' + str(right_count))
            if FeatureExtractor._check_informative(dep_left_most):
               result.append('BUF_1_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
               result.append('BUF_1_RDEP_' + dep_right_most)

        if stack and buffer :
	   buffer_idx0 = buffer[0]
	   stack_idx0 = stack[-1]
           
           token_buff = tokens[buffer_idx0]
           token_stack =  tokens[stack_idx0]

           if len(buffer) > 1:
               buffer_idx1 = buffer[1]
               token_buff1 = tokens[buffer_idx1]
               if 'tag' in token_buff and 'tag' in token_buff1 and 'tag' in token_stack and FeatureExtractor._check_informative(token_stack['tag']) and FeatureExtractor._check_informative(token_buff['tag']) and FeatureExtractor._check_informative(token_buff1['tag']):
			result.append('TAG_STACK0_BUFF01_' + token_stack['tag'] + token_buff['tag'] + token_buff1['tag'])
#               if 'tag' in token_buff and 'tag' in token_buff1 and 'tag' in token_stack and FeatureExtractor._check_informative(token_stack['tag']) and FeatureExtractor._check_informative(token_buff['tag']) and FeatureExtractor._check_informative(token_buff1['tag']):
 #                       result.append('TAGWORD_STACK0_BUFF01_' + token_stack['tag'] + token_stack['word'] +  token_buff['tag'] +token_buff['word'] + token_buff1['tag'] + tokenbuff1['word'])
               
               
           #if len(stack) > 1:
	#	 stack_idx1 = stack[-2]
         #  if len(buffer) >2:
          #       buffer_idx2 = buffer[2]
          # if len(stack) > 2:
	#	 stack_idx2 = stack[-3]
  
           
           #token_buff = tokens[buffer_idx0]
           #token_stack =  tokens[stack_idx0]
           
           
           dist = token_buff['address'] - token_stack['address']
           result.append('STK0_BUFF0_DIST_' + str(dist))
  
	
        return result
