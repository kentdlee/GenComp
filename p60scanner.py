from scanner import *
from state import *

#TOKEN Constants
TokenToIDMap = {'a':0,'b':1,'d':2,'f':3,'x':4,'z':5,'eof':6}
IDToTokenMap = {0:'a',1:'b',2:'d',3:'f',4:'x',5:'z',6:'eof'}

#KEYWORD Constants

class p60Scanner(Scanner):
	def __init__(self,instream):
		super().__init__(instream,0,{0: State(0,None,[('EOF', 1), ('a', 2), ('b', 3), ('d', 4), ('f', 5), ('x', 6), ('z', 7)]), 1: State(1,6,[]), 2: State(2,0,[]), 3: State(3,1,[]), 4: State(4,2,[]), 5: State(5,3,[]), 6: State(6,4,[]), 7: State(7,5,[])},{'EOF': OrderedSet({3}), 'EPSILON': OrderedSet(), 'd': OrderedSet({100}), 'b': OrderedSet({98}), 'f': OrderedSet({102}), 'x': OrderedSet({120}), 'a': OrderedSet({97}), 'z': OrderedSet({122})},{},6,False)

