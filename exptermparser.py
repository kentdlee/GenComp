from expressionbackend import *
from parser import *

class exptermParser(Parser):
	def __init__(self):
		super().__init__({0: LR0State(0,frozenset({LR0Item(0,Production(0,7,[8, 6],'E'),0,set()), LR0Item(1,Production(1,8,[8, 3, 9],'Add(E,T)'),0,set()), LR0Item(2,Production(2,8,[8, 4, 9],'Sub(E,T)'),0,set()), LR0Item(3,Production(3,8,[9],'T'),0,set()), LR0Item(4,Production(4,9,[0],'Num(number)'),0,set()), LR0Item(5,Production(5,9,[1, 8, 2],'E'),0,set())}),{8: 1, 9: 2, 0: 3, 1: 4},False), 1: LR0State(1,frozenset({LR0Item(6,Production(0,7,[8, 6],'E'),1,set()), LR0Item(6,Production(1,8,[8, 3, 9],'Add(E,T)'),1,set()), LR0Item(6,Production(2,8,[8, 4, 9],'Sub(E,T)'),1,set())}),{3: 7, 4: 8, 6: 11},False), 2: LR0State(2,frozenset({LR0Item(6,Production(3,8,[9],'T'),1,{2, 3, 4, 6})}),{},False), 3: LR0State(3,frozenset({LR0Item(6,Production(4,9,[0],'Num(number)'),1,{2, 3, 4, 6})}),{},False), 4: LR0State(4,frozenset({LR0Item(1,Production(1,8,[8, 3, 9],'Add(E,T)'),0,set()), LR0Item(6,Production(5,9,[1, 8, 2],'E'),1,set()), LR0Item(2,Production(2,8,[8, 4, 9],'Sub(E,T)'),0,set()), LR0Item(3,Production(3,8,[9],'T'),0,set()), LR0Item(4,Production(4,9,[0],'Num(number)'),0,set()), LR0Item(5,Production(5,9,[1, 8, 2],'E'),0,set())}),{8: 5, 9: 2, 0: 3, 1: 4},False), 5: LR0State(5,frozenset({LR0Item(6,Production(1,8,[8, 3, 9],'Add(E,T)'),1,set()), LR0Item(6,Production(5,9,[1, 8, 2],'E'),2,set()), LR0Item(6,Production(2,8,[8, 4, 9],'Sub(E,T)'),1,set())}),{2: 6, 3: 7, 4: 8},False), 6: LR0State(6,frozenset({LR0Item(3,Production(5,9,[1, 8, 2],'E'),3,{2, 3, 4, 6})}),{},False), 7: LR0State(7,frozenset({LR0Item(1,Production(4,9,[0],'Num(number)'),0,set()), LR0Item(2,Production(5,9,[1, 8, 2],'E'),0,set()), LR0Item(3,Production(1,8,[8, 3, 9],'Add(E,T)'),2,set())}),{0: 3, 1: 4, 9: 9},False), 8: LR0State(8,frozenset({LR0Item(1,Production(4,9,[0],'Num(number)'),0,set()), LR0Item(2,Production(5,9,[1, 8, 2],'E'),0,set()), LR0Item(3,Production(2,8,[8, 4, 9],'Sub(E,T)'),2,set())}),{0: 3, 1: 4, 9: 10},False), 9: LR0State(9,frozenset({LR0Item(3,Production(1,8,[8, 3, 9],'Add(E,T)'),3,{2, 3, 4, 6})}),{},False), 10: LR0State(10,frozenset({LR0Item(3,Production(2,8,[8, 4, 9],'Sub(E,T)'),3,{2, 3, 4, 6})}),{},False), 11: LR0State(11,frozenset({LR0Item(3,Production(0,7,[8, 6],'E'),2,set())}),{},True)},['number', "'('", "')'", "'+'", "'-'", "'*'", 'endoffile', 'Start', 'E', 'T'])

	def eval(self,expression):
		return eval(expression)