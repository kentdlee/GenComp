from genscanner import *
from state import *

#TOKEN Constants
TokenToIDMap = {'number':0,'(':1,')':2,'+':3,'-':4,'*':5,'endoffile':6}
IDToTokenMap = {0:'number',1:'(',2:')',3:'+',4:'-',5:'*',6:'endoffile'}

#KEYWORD Constants

class exptermScanner(Scanner):
	def __init__(self,instream):
		super().__init__(instream,0,{0: State(0,None,{'(': 1, '+': 4, '*': 3, '-': 5, 'digit': 7, 'EOF': 6, ')': 2}), 1: State(1,1,{}), 2: State(2,2,{}), 3: State(3,5,{}), 4: State(4,3,{}), 5: State(5,4,{}), 6: State(6,6,{}), 7: State(7,0,{'digit': 7})},{'(': OrderedSet({40}), '+': OrderedSet({43}), '*': OrderedSet({42}), 'digit': OrderedSet({48, 49, 50, 51, 52, 53, 54, 55, 56, 57}), '-': OrderedSet({45}), ')': OrderedSet({41}), 'EOF': OrderedSet({3}), 'EPSILON': OrderedSet()},{},0,False)

