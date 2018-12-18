from jpythonbackend import *
from genparser import *

class listParser(Parser):
	def __init__(self):
		super().__init__({0: LR0State(0,frozenset({LR0Item(0,Production(0,2,[3],'block(Block)'),0,set())}),{3: 1},False), 1: LR0State(1,frozenset({LR0Item(1,Production(0,2,[3],'block(Block)'),1,set())}),{},True)},["','", 'endoffile', 'List', 'element'])

	def eval(self,expression):
		return eval(expression)
