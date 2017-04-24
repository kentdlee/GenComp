from scanner import *
from state import *

#TOKEN Constants
TokenToIDMap = {'number':0,'+':1,'*':2,'endoffile':3}
IDToTokenMap = {0:'number',1:'+',2:'*',3:'endoffile'}

#KEYWORD Constants

class postfixScanner(Scanner):
	def __init__(self,instream):
		super().__init__(instream,0,{0: State(0,None,{'EOF': 3, '+': 2, '*': 1, 'digit': 4}), 1: State(1,2,{}), 2: State(2,1,{}), 3: State(3,3,{}), 4: State(4,0,{'digit': 4})},{'EPSILON': OrderedSet(), 'EOF': OrderedSet({3}), '+': OrderedSet({43}), '*': OrderedSet({42}), 'digit': OrderedSet({48, 49, 50, 51, 52, 53, 54, 55, 56, 57})},{},0,False)

