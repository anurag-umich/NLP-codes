class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	if not conf.buffer or not conf.stack:
            return -1
	buff = conf.buffer[0]
	sigma = conf.stack[-1]
	if sigma == 0:
	   return -1
	if sum([sigma == j for i, l, j in conf.arcs]):
		return -1
	conf.stack.pop()
	conf.arcs.append((buff, relation, sigma))
       # raise NotImplementedError('Please implement left_arc!')
        #return -1

    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer or not conf.stack:
            return -1

        # You get this one for free! Use it as an example.

        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        conf.stack.append(idx_wj)
        conf.arcs.append((idx_wi, relation, idx_wj))

    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	if not conf.buffer or not conf.stack:
            return -1
       # raise NotImplementedError('Please implement reduce!')
	sigma = conf.stack[-1]
	if sum([sigma == j for i, l, j in conf.arcs]):
            conf.stack.pop()
        else:
            return -1
        

    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	if not conf.buffer or not conf.stack:
            return -1
        
        conf.stack.append(conf.buffer[0])
	conf.buffer.pop(0)
       # raise NotImplementedError('Please implement shift!')
       