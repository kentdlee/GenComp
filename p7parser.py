
from genparser import *

class p7Parser(Parser):
	def __init__(self):
		super().__init__({0: LR0State(0,frozenset({LR0Item(0,Production(0,3,[4, 2],'OneOrTwo'),0,set()), LR0Item(1,Production(1,4,[0],'one'),0,set()), LR0Item(2,Production(2,4,[1],'two'),0,set())}),{0: 1, 1: 2, 4: 3},False), 1: LR0State(1,frozenset({LR0Item(3,Production(1,4,[0],'one'),1,{2})}),{},False), 2: LR0State(2,frozenset({LR0Item(3,Production(2,4,[1],'two'),1,{2})}),{},False), 3: LR0State(3,frozenset({LR0Item(3,Production(0,3,[4, 2],'OneOrTwo'),1,set())}),{2: 4},False), 4: LR0State(4,frozenset({LR0Item(1,Production(0,3,[4, 2],'OneOrTwo'),2,set())}),{},True)},['one', 'two', 'eof', 'Prog', 'OneOrTwo'])

	def eval(self,expression):
		return eval(expression)
