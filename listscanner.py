from genscanner import *
from state import *

#TOKEN Constants
TokenToIDMap = {',':0,'endoffile':1}
IDToTokenMap = {0:',',1:'endoffile'}

#KEYWORD Constants

class listScanner(Scanner):
	def __init__(self,instream):
		super().__init__(instream,0,{0: State(0,None,{',': 1, 'EOF': 2}), 1: State(1,0,{}), 2: State(2,1,{})},{'EPSILON': OrderedSet(), 'digit': OrderedSet({48, 49, 50, 51, 52, 53, 54, 55, 56, 57}), 'EOF': OrderedSet({3}), ',': OrderedSet({44})},{},1,False)

