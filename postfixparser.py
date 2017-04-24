from expressionbackend import *
from parser import *

class postfixParser(Parser):
	def __init__(self):
		super().__init__({0: LR0State(0,frozenset({LR0Item(0,Production(0,4,[5, 3],'E'),0,set()), LR0Item(1,Production(1,5,[5, 5, 1],'Add(E1,E2)'),0,set()), LR0Item(2,Production(2,5,[5, 5, 2],'Mul(E1,E2)'),0,set()), LR0Item(3,Production(3,5,[0],'Num(number)'),0,set())}),{0: 1, 5: 2},False), 1: LR0State(1,frozenset({LR0Item(4,Production(3,5,[0],'Num(number)'),1,{0, 1, 2, 3})}),{},False), 2: LR0State(2,frozenset({LR0Item(3,Production(1,5,[5, 5, 1],'Add(E1,E2)'),0,set()), LR0Item(4,Production(0,4,[5, 3],'E'),1,set()), LR0Item(4,Production(1,5,[5, 5, 1],'Add(E1,E2)'),1,set()), LR0Item(4,Production(2,5,[5, 5, 2],'Mul(E1,E2)'),1,set()), LR0Item(4,Production(2,5,[5, 5, 2],'Mul(E1,E2)'),0,set()), LR0Item(5,Production(3,5,[0],'Num(number)'),0,set())}),{0: 1, 3: 3, 5: 4},False), 3: LR0State(3,frozenset({LR0Item(6,Production(0,4,[5, 3],'E'),2,set())}),{},True), 4: LR0State(4,frozenset({LR0Item(4,Production(1,5,[5, 5, 1],'Add(E1,E2)'),0,set()), LR0Item(6,Production(1,5,[5, 5, 1],'Add(E1,E2)'),1,set()), LR0Item(6,Production(1,5,[5, 5, 1],'Add(E1,E2)'),2,set()), LR0Item(6,Production(2,5,[5, 5, 2],'Mul(E1,E2)'),2,set()), LR0Item(6,Production(2,5,[5, 5, 2],'Mul(E1,E2)'),1,set()), LR0Item(5,Production(2,5,[5, 5, 2],'Mul(E1,E2)'),0,set()), LR0Item(6,Production(3,5,[0],'Num(number)'),0,set())}),{0: 1, 1: 5, 2: 6, 5: 4},False), 5: LR0State(5,frozenset({LR0Item(7,Production(1,5,[5, 5, 1],'Add(E1,E2)'),3,{0, 1, 2, 3})}),{},False), 6: LR0State(6,frozenset({LR0Item(7,Production(2,5,[5, 5, 2],'Mul(E1,E2)'),3,{0, 1, 2, 3})}),{},False)},['number', "'+'", "'*'", 'endoffile', 'Start', 'E'])

	def eval(self,expression):
		return eval(expression)
