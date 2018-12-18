from genscanner import *
from state import *

#TOKEN Constants
TokenToIDMap = {'one':0,'two':1,'eof':2}
IDToTokenMap = {0:'one',1:'two',2:'eof'}

#KEYWORD Constants

class p7Scanner(Scanner):
	def __init__(self,instream):
		super().__init__(instream,0,{0: State(0,None,{'EOF': 1, 'a': 4}), 1: State(1,2,{}), 2: State(2,1,{'a': 3}), 3: State(3,0,{'a': 5, 'b': 6}), 4: State(4,None,{'b': 2}), 5: State(5,1,{'a': 5}), 6: State(6,0,{'b': 6})},{'EPSILON': OrderedSet(), 'EOF': OrderedSet({3}), 'a': OrderedSet({97}), 'b': OrderedSet({98})},{},0,False)

