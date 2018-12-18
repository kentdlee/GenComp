from genscanner import *
from state import *

#TOKEN Constants
TokenToIDMap = {'L':15,'endoffile':16}
IDToTokenMap = {15:'L',16:'endoffile'}

#KEYWORD Constants
False_keyword=14
None_keyword=9
True_keyword=13
and_keyword=4
decl_keyword=12
def_keyword=0
else_keyword=11
for_keyword=10
if_keyword=1
in_keyword=8
len_keyword=3
not_keyword=5
or_keyword=6
return_keyword=7
while_keyword=2

class classexampleScanner(Scanner):
	def __init__(self,instream):
		super().__init__(instream,0,{0: State(0,None,{'A': 3}), 1: State(1,15,{'A': 0, 'EOF': 2, 'B': 3}), 2: State(2,16,{}), 3: State(3,15,{'A': 0})},{'A': OrderedSet({97}), 'EOF': OrderedSet({3}), 'B': OrderedSet({98}), 'EPSILON': OrderedSet()},{'True': 13, 'for': 10, 'else': 11, 'def': 0, 'return': 7, 'if': 1, 'in': 8, 'and': 4, 'while': 2, 'not': 5, 'None': 9, 'decl': 12, 'False': 14, 'len': 3, 'or': 6},15,False)

