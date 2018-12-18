# Parsegen:
# written by Kent D. Lee
# email: kentdlee@gmail.com
# License - Free for non-commercial, educational use.
# (c) 2016
# This program may be used in part or its entirety for non-commercial, educational
# purposes.

import sys
import stack
import streamreader
from lr0state import *


class ParserGenerator:
    def __init__(self):
        self.tntMap = {}
        self.tnts = []
        self.productions = []
        self.terminals = set()
        self.nonterminals = set()
        self.states = {}
        self.itemsToStateId = {}
        self.definitions = ""


    def readInputFile(self,instream):
        def addNonterminal(nonterminal):
            if not nonterminal in self.nonterminals:
                self.nonterminals.add(nonterminal)
                self.tnts.append(nonterminal)
                self.tntMap[nonterminal] = len(self.tnts) - 1

        def readRHS(prod):
            while not reader.peek("("):
                if reader.peek("'"): # This is a token that starts with a quote.
                    reader.readUpTo("'")
                    terminal = "'" + reader.readUpTo("'")
                    #print("Found terminal", terminal)
                    if not terminal in self.terminals:
                        raise Exception("Undefined terminal: " + terminal)
                    prod.addRHSItem(self.tntMap[terminal])

                else:
                    tntName = reader.readIdentifier()
                    #print("Found item", tntName)

                    if tntName != "null":
                        if not tntName in self.terminals:
                            addNonterminal(tntName)
                        prod.addRHSItem(self.tntMap[tntName])

            reader.readUpTo("(")
            returnValue = reader.readUpTo(");")[:-2]
            if returnValue.count("::=") > 0:
                raise Exception("Found ::= within production return value. Likely a ; is missing at the end of line " + str(reader.getLineNumber()-1) + ".")
            prod.returnValue = returnValue

        reader = streamreader.StreamReader(instream)
        index = 0

        reader.readUpTo("#")

        while not (reader.peek("KEYWORDS") or reader.peek("TOKENS")):
            reader.readUpTo("#")

        if reader.peek("KEYWORDS"):
            reader.readUpTo("KEYWORDS")
            #print("Found Keywords in file.")
            reader.skipComments()

            while reader.peek("'"):
                reader.readUpTo("'")

                keyword = "'" + reader.readUpTo("'")
                self.terminals.add(keyword)
                self.tnts.append(keyword)
                self.tntMap[keyword] = len(self.tnts)-1
                reader.readUpTo(";")
                reader.skipComments()

            reader.readUpTo("#TOKENS")
        else:
            reader.readUpTo("TOKENS")
        #print("Keywords=", self.terminals)
        reader.skipComments()

        while (not reader.peek("#DEFINITIONS")) and (not reader.peek("#PRODUCTIONS")):
            if reader.peek("'"):
                reader.readUpTo("'")
                tokenName = "'" + reader.readUpTo("'")
            else:
                tokenName = reader.readIdentifier()

            self.tnts.append(tokenName)
            self.terminals.add(tokenName)
            self.tntMap[tokenName] = len(self.tnts)-1

            reader.readUpTo(";")
            reader.skipComments()

        #print(self.tnts)
        #print(self.tntMap)
        #print(self.terminals)

        if reader.peek("#DEFINITIONS"):
            reader.readUpTo("#DEFINITIONS")

            self.definitions = reader.readUpTo("#PRODUCTIONS")[:-len("#PRODUCTIONS")]

        else:
            self.definitions = ""
            reader.readUpTo("#PRODUCTIONS")

        # Add the goal nonterminal and production
        # before reading the other productions.
        #addNonterminal("$$GOAL$$")
        #prod = Production(0,self.tntMap["$$GOAL$$"])
        #prod.addRHSItem(len(self.terminals)+1)
        #prod.tnts = self.tnts
        #prod.terminals = self.terminals
        #self.productions.append(prod)

        while not reader.peek("#END"):
            lhsName = reader.readIdentifier()
            addNonterminal(lhsName)

            prod = Production(len(self.productions),self.tntMap[lhsName])
            prod.tnts = self.tnts
            prod.terminals = self.terminals
            self.productions.append(prod)
            reader.readUpTo("::=")
            readRHS(prod)

            while reader.peek("|"):
                prod = Production(len(self.productions),self.tntMap[lhsName])
                prod.tnts = self.tnts
                prod.terminals = self.terminals
                self.productions.append(prod)
                reader.readUpTo("|")
                readRHS(prod)


        reader.readUpTo("#END")

        #for p in self.productions:
        #    print(p)


    def buildParser(self):

        # DESCRIPTION- COMPLETION COMPLETES A STATE BY FINDING ALL ADDITIONAL
        # PRODUCTIONS THAT SHOULD BE INCLUDED IN THE STATE'S
        # EQUIVALENCE CLASS. THIS OPERATION IS DESCRIBED IN
        # COMPILER CONSTRUCTION THEORY AND PRACTICE ON PAGE
        # 230 AND IN COMPILER WRITING ON PAGE 351.
        def completion(theState):
            changes = True
            while changes:
                changes = False
                origItemSet = set(theState.items)
                for lr0Item in origItemSet:
                    # if there is a terminal/nonterminal to the right
                    # of the dot in the item then ...
                    if lr0Item.dotIndex < len(lr0Item.production.rhs):
                        for production in self.productions:
                            if production.lhsId == lr0Item.production.rhs[lr0Item.dotIndex]:
                                # Create a new LR0 Item to add to the set of productions
                                # with its dot at the left hand side if the item is not
                                # already in the item set of the state.
                                newlr0Item = LR0Item(len(theState.items),production)
                                newlr0Item.tnts = self.tnts
                                if not newlr0Item in theState.items:
                                    theState.items.add(newlr0Item)
                                    changes = True
            theState.items = frozenset(theState.items)
            return theState

        # DESCRIPTION- SUCCESSOR FINDS THE ITEM SET THAT IS FORMED BY DOING A
        # READ OPERATION ON THE GIVEN STATE ITEM SET. THE COMPLETION
        # PROCEDURE IS USED TO COMPLETE THE STATE SET AFTER ONE
        # ITEM HAS BEEN FOUND IN THAT SET. THIS OPERATION IS
        # ALSO DESCRIBED ON THE SAME PAGES AS MENTIONED IN THE
        # COMPLETION OPERATION DESCRIPTION.
        # For efficiency we will make one pass through the items of a state
        # and build a map from terminal/nonterminal to the set of new items
        def successors(theState):
            successorSet = set()
            successorItems = {}

            for lr0Item in theState.items:
                if lr0Item.dotIndex < len(lr0Item.production.rhs):
                    tnt = lr0Item.production.rhs[lr0Item.dotIndex]
                    newlr0Item = LR0Item(len(theState.items), lr0Item.production, lr0Item.dotIndex+1)
                    newlr0Item.tnts = self.tnts
                    if not tnt in successorItems:
                        successorItems[tnt] = set([newlr0Item])
                    else:
                        successorItems[tnt].add(newlr0Item)

            for tnt in successorItems:
                # make a new state so completion can be called
                # we might use this state, but we will figure that
                # out below.
                stateId = len(self.states)
                nextState = completion(LR0State(stateId,successorItems[tnt]))
                nextState.tnts = self.tnts
                itemSet = nextState.items

                if itemSet in self.itemsToStateId:
                    nextState = self.states[self.itemsToStateId[itemSet]]
                else:
                    # use the new state
                    self.states[stateId] = nextState
                    self.itemsToStateId[nextState.items] = stateId
                    successorSet.add(stateId)

                # The addTransition function must have the new state
                # passed to it since it needs to set the predecessor
                # to it as well.
                theState.addTransition(tnt, nextState)

            return successorSet

        def buildLR0Machine():
            # Build an initial LR0 Item with the first production
            # in it.
            lr0Item = LR0Item(0,self.productions[0])
            lr0Item.tnts = self.tnts
            theState = LR0State(0,set([lr0Item]))
            theState.tnts = self.tnts
            self.states[0] = completion(theState)
            self.itemsToStateId[theState.items] = 0

            unexploredStates = stack.Stack()
            unexploredStates.push(0)
            while not unexploredStates.isEmpty():
                stateId = unexploredStates.pop()
                theState = self.states[stateId]
                newStates = successors(theState)
                for stateId in newStates:
                    unexploredStates.push(stateId)

        # DESCRIPTION - AS DEFINED ON PAGE 62 OF THE PAPER MENTIONED IN THE
        # LOOK_AHEAD DESCRIPTION. THIS FUNCTION, GIVEN A STATE
        # AND AN INPUT STRING, RETURNS ALL STATES THAT ARE
        # VISITED UPON EVALUATING THE STRING SUCH THAT THE
        # FINAL STATE VISITED UPON EVALUATING THE STRING IS
        # THE STATE PASSED TO THE FUNCTION TO BEGIN WITH.
        # In this version of this function, the state keeps track of its
        # predecessor states so we can go backwards through it to find
        # the predecessor states. This makes the algorithm much more efficient
        # in time while using twice as much space for transitions (which is
        # relatively small).
        # NOTE: The one possible problem with this version of the algorithm
        # would arise if a state has mulitiple predecessors on a given
        # terminal or nonterminal. However, an exception would be thrown
        # in that case (it is raised by the addTransition method on LR0State).
        def pred(stateId,alpha):

            theState = self.states[stateId]

            if len(alpha) == 0:
                return frozenset([stateId])

            alphaprime = alpha[:-1]
            X = alpha[-1]

            predecessors = set()
            for stateId in theState.pred(X):
                predecessors.update(pred(stateId,alphaprime))

            return frozenset(predecessors)


        # DESCRIPTION - AS DEFINED ON PAGE 61 OF COMPILER WRITING (TREMBLAY
        # AND SORENSON). THIS PROCEDURE COMPUTES THE SET OF
        # NULLABLE NONTERMINALS AND STORES THEM IN THE GLOBAL
        # SET NULL_SET.
        # This set must contain any null nonterminals and any nonterminals
        # that go could go to null because their rhs is composed only of
        # nullable nonterminals.
        def nullableRHS(prod,nullset):
            for tnt in prod.rhs:
                if not tnt in nullset:
                    return False

            return True

        def empty():
            nullset = set()
            for prod in self.productions:
                if len(prod.rhs) == 0:
                    nullset.add(prod.id)

            changes = True
            while changes:
                changes = False
                for prod in self.productions:
                    if not prod.id in nullset and nullableRHS(prod,nullset):
                        nullset.add(prod.id)
                        changes=True

            return nullset


        # lalr1 returns a set of Sigma - A Set of Terminals
        # item is an LR0Item and stateId is an LR0 state id

        def lalr1(item, stateId):

            def nullable(string):
                for alpha in string:
                    if not alpha in nullset:
                        return False

                return True

            # DESCRIPTION - AS DESCRIBED ON PAGE 67 OF THE ACM PAPER.
            # THIS PROCEDURE IS USED IN CALCULATING THE
            # LOOKAHEAD SETS BASED ON TRANSITION INFORMATION
            # OF PREDECESSOR STATES.

            def trans(stateId):
                if stateId == -1:
                    # No transition so return
                    return
                # stateId is an LR0 State state id
                tm.add(stateId)
                theState = self.states[stateId]
                for item in theState.items:
                    if item.dotIndex < len(item.production.rhs):
                        # tnt is X from the paper
                        tnt = item.production.rhs[item.dotIndex]
                        nextStateId = theState.onClassGoTo(tnt)
                        if self.tnts[tnt] in self.terminals:
                            la.add(tnt)
                        else:
                            if tnt in nullset and not nextStateId in tm:
                                trans(nextStateId)


            # stateId is the id of an LR0State. The index is the index of an item in the state.

            def lalr(item, stateId):
                theState = self.states[stateId]
                done.add((item.id,stateId))
                for predStateId in pred(stateId, item.production.rhs[:item.dotIndex]):
                    predState = self.states[predStateId]
                    nextStateId = predState.onClassGoTo(item.production.lhsId)
                    trans(nextStateId)
                    for predItem in predState.items:
                        if len(predItem.production.rhs) > predItem.dotIndex and predItem.production.rhs[predItem.dotIndex] == item.production.lhsId:
                            psi = predItem.production.rhs[predItem.dotIndex+1:]
                            if nullable(psi) and not (predItem.id,predStateId) in done:
                                # this is an optimization of the algorithm since
                                # lalr looks at predecessors in the lr0 machine and
                                # there are no predecessor states if the dot is already
                                # at the left-most end.
                                # if predItem.dotIndex > 0:
                                lalr(predItem,predStateId)

            # beginning of lalr1
            done = set()
            la = set()
            tm = set()
            #if self.tnts[item.production.lhsId] == '$$GOAL$$': # then this is the $$GOAL$$ nonterminal
            #    la.add(len(self.terminals))
            #else:
            lalr(item, stateId)

            return la


        # Beginning of buildParser. Here we initialize any needed
        # variables.
        buildLR0Machine()
        nullset = empty()
        for stateId in self.states:
            theState = self.states[stateId]
            termSet = set(theState.transitions.keys())
            laSet = set()

            for item in theState.items:
                if item.dotIndex == len(item.production.rhs):
                    item.la = lalr1(item,stateId)

                    for laVal in item.la:
                        if laVal in termSet:
                            sys.stderr.write("Warning: There is a shift/reduce conflict in state " + str(theState.id) + " on terminal " + self.tnts[laVal] + "\n")
                            sys.stderr.write("         Conflict will be resolved by shifting.\n")
                        if laVal in laSet:
                            sys.stderr.write("Error: There is a reduce/reduce conflict in state " + str(theState.id) + " on terminal " + self.tnts[laVal] + "\n")

                    laSet.update(item.la)

                    if item.production.lhsId == len(self.terminals):
                        # This is the start production with the dot
                        # at the right end, so this is the accepting state
                        theState.accepting = True



    def writeListing(self,strm):
        for stateId in self.states:
            theState = self.states[stateId]
            strm.write(str(theState)+"\n")

    def writeParser(self,strm,prefix):
        strm.write(self.definitions.strip()+"\n")
        strm.write("from genparser import *\n\n")

        strm.write("class " + prefix + "Parser(Parser):\n")
        strm.write("\tdef __init__(self):\n")
        strm.write("\t\tsuper().__init__("+repr(self.states)+","+repr(self.tnts)+")\n\n")

        # The following defines an inherited eval method so that
        # parser return values can be evaluated in the scope of this module.
        # This enables an abstract syntax tree to be evaluated in the scope
        # of the backend code found in the #Definitions section of the gencomp 
        # file.
        strm.write("\tdef eval(self,expression):\n")
        strm.write("\t\treturn eval(expression)\n")


def main():

    if len(sys.argv) != 2:
        print("usage: parsegen inputfile")
        return

    filename = sys.argv[1]

    lst = filename.split(".")
    outputFilename = lst[0] + "parser.py"
    instream = open(filename,'r')
    outstream = open(outputFilename,"w")

    gen = ParserGenerator()
    gen.readInputFile(instream)
    gen.buildParser()


    gen.writeListing(sys.stdout)
    gen.writeParser(outstream,lst[0])

    outstream.close()


    print("Parsegen completed.")

if __name__ == "__main__":
    main()
