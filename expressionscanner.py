from genscanner import *
from state import *

#TOKEN Constants
TokenToIDMap = {'number':0,'(':1,')':2,'+':3,'*':4,'endoffile':5}
IDToTokenMap = {0:'number',1:'(',2:')',3:'+',4:'*',5:'endoffile'}

#KEYWORD Constants

class expressionScanner(Scanner):
	def __init__(self,instream):
		super().__init__(instream,0,{0: State(0,None,{'EOF': 5, 'digit': 6, '+': 4, '(': 1, ')': 2, '*': 3}), 1: State(1,1,{}), 2: State(2,2,{}), 3: State(3,4,{}), 4: State(4,3,{}), 5: State(5,5,{}), 6: State(6,0,{'digit': 6})},{'EOF': OrderedSet({3}), 'digit': OrderedSet({48, 49, 50, 51, 52, 53, 54, 55, 56, 57}), '+': OrderedSet({43}), '(': OrderedSet({40}), 'EPSILON': OrderedSet(), ')': OrderedSet({41}), '*': OrderedSet({42})},{},0,False)

