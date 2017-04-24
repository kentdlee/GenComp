# Scangen: 
# written by Kent D. Lee
# email: kentdlee@gmail.com
# License - Free for non-commercial, educational use. 
# (c) 2016
# This program may be used in part or its entirety for non-commercial, educational 
# purposes. 

import sys
import stack
import state
import nfastate
import streamreader
import orderedcollections

epsilon = "EPSILON"

class Operator:
    def __init__(self,op):
        self.op = op
 
    def precedence(self):
        if self.op == "|":
            return 1
        if self.op == ".":
            return 2
        if self.op == "*":
            return 3
        if self.op == "(" or self.op == ")":
            return 0

    def getOpChar(self):
        return self.op 

   
class NFA:
    def __init__(self, classes = {epsilon:orderedcollections.OrderedSet()}, states = orderedcollections.OrderedMap(), keywords = orderedcollections.OrderedMap(), tokens = orderedcollections.OrderedMap(), firstTokenId = -1 ):
        self.classes = orderedcollections.OrderedMap(classes)
        self.states = orderedcollections.OrderedMap(states)
        self.numStates = len(states)
        self.keywords = orderedcollections.OrderedMap(keywords)
        self.tokens = orderedcollections.OrderedMap(tokens)
        self.firstTokenId = firstTokenId
        
    def __repr__(self):
        return ("NFA(" + repr(self.classes) + "," + repr(self.states) + "," + repr(self.keywords) + "," + repr(self.tokens) + "," + repr(self.firstTokenId) + ")")
        
    def getFirstTokenId(self):
        return self.firstTokenId     
        
    def buildMachine(self,instream):

        
        def operate(op,opStack,stateStack):
        
            #print "Operating..."
            #print "The operator is ", op.getOpChar()
        
            if (op.getOpChar() == '('):
                opStack.push(Operator('('))
                return
        
            while op.precedence() <= opStack.peek().precedence():
                topOp = opStack.pop()
        
                opChar = topOp.getOpChar()
        
                #print "The topOp is ", opChar
        
                if opChar == '|':
                    b1,b2 = stateStack.pop()
                    a1,a2 = stateStack.pop()
                    firstId = newState()
                    secondId = newState()
                    self.states[firstId].addTransition(epsilon,a1)
                    self.states[firstId].addTransition(epsilon,b1)
                    self.states[a2].addTransition(epsilon,secondId)
                    self.states[b2].addTransition(epsilon,secondId)
                    stateStack.push((firstId,secondId))
                elif opChar == '.':
                    b1,b2 = stateStack.pop()
                    a1,a2 = stateStack.pop()
                    firstId = newState()
                    secondId = newState()
                    self.states[firstId].addTransition(epsilon,a1)
                    self.states[a2].addTransition(epsilon,b1)
                    self.states[b2].addTransition(epsilon,secondId)  
                    stateStack.push((firstId,secondId))
                elif opChar == '*':
                    a1,a2 = stateStack.pop()
                    firstId = newState()
                    secondId = newState()
                    self.states[firstId].addTransition(epsilon,a1)
                    self.states[firstId].addTransition(epsilon,secondId)                    
                    self.states[a2].addTransition(epsilon,secondId)
                    self.states[secondId].addTransition(epsilon,firstId)  
                    stateStack.push((firstId,secondId))
                elif opChar == '(':
                    # do nothing 
                    if (op.getOpChar() == ')'):
                        return
        
            opStack.push(op)
            
        def evaluateRegExpression(reader):
            opStack = stack.Stack()
            stateStack = stack.Stack()
            
            opStack.push(Operator("("))
            
            
            while not reader.peek(";"):
                if reader.peek("(") or reader.peek(")") or reader.peek(".") or reader.peek("*") or reader.peek("|"):
                    token = reader.readChar()
                    op = Operator(token)
                    operate(op, opStack, stateStack)                
        
                else: # it is a character class set name
                    ident = reader.readIdentifier()
                    firstId = newState()
                    secondId = newState()
                    self.states[firstId].addTransition(ident, secondId)
                    stateStack.push((firstId,secondId))
            
            operate(Operator(')'), opStack, stateStack)
            
            if (not opStack.isEmpty()):
                raise Exception("Malformed Regular Expression")
        
            return stateStack.pop()
        
        def newState():
            self.numStates+=1
            aState = nfastate.NFAState(self.numStates)
            self.states[self.numStates] = aState
            return self.numStates
            
        
        reader = streamreader.StreamReader(instream)
        startStates = []
        
        reader.skipComments()
            
        if reader.peek("#CLASSES"):
            #print("Found #CLASSES")
            reader.readUpTo("\n")
            while (not reader.peek("#")):
                # The "#" marks the beginning of the next section. Either KEYWORDS or TOKENS. KEYWORDS are optional.
                reader.skipComments()
                
                # We could have keywords right after a comment. So if keyword section is found, don't read
                # any more character classes.
                if not reader.peek("#KEYWORDS"):
                    className = reader.readIdentifier()
                    reader.readUpTo("=")
                    if reader.peek("^"):
                        anticlass = True
                        reader.readUpTo("^")
                        classSet = orderedcollections.OrderedSet(range(256))
                    else:
                        anticlass = False
                        classSet = orderedcollections.OrderedSet()
                        
                    done = False
                        
                    while not done:
                    
                        if reader.peek("'"):
                            # Found a character constant
                            reader.readUpTo("'")
                            character = reader.readUpTo("'")[0]
                            #print(character)
                            ordVal = ord(character)
                            
                        else:
                            ordVal = reader.readInt()
                            
                        # Add the end of the range if there is a range of characters
                        if reader.peek(".."):
                            reader.readUpTo("..")
             
                            if reader.peek("'"):
                                reader.readUpTo("'")
                                character = reader.readUpTo("'")[0]
                                #print(character)
                                lastOrdVal = ord(character)
                            else:
                                lastOrdVal = reader.readInt()
                        else:
                            lastOrdVal = ordVal
                            
                        # Now build the set
                        for i in range(ordVal, lastOrdVal+1):
                            if anticlass:
                                classSet.remove(i)
                            else:
                                classSet.add(i)
                            
                        if reader.peek(","):
                            reader.readUpTo(",")
                        else:
                            done = True      
                         
                    #print(className)
                    
                    #Add the class to the class dictionary
                    self.classes[className] = classSet
                    
                    reader.readUpTo(";")
                    
           
        #print("These are the classes")         
        #print(self.classes)
        # keyword and token id numbers
        idnum = 0
        keywordsPresent = False
        
        if reader.peek("#KEYWORDS"):
            reader.readUpTo("#KEYWORDS")
            keywordsPresent = True
            reader.skipComments()
        
            while (not reader.peek("#TOKENS")):
                #idnum = reader.readInt()
                #reader.readUpTo(":")
                reader.readUpTo("'")
                keyword = reader.readUpTo("'")[:-1].strip()
                #print(idnum,keyword)
                self.keywords[keyword] = idnum
                idnum += 1
                reader.readUpTo(";")
                reader.skipComments()
             
        #print(self.keywords)
        reader.readUpTo("#TOKENS")
        reader.skipComments()
        readingFirstToken = True

        while not (reader.peek("#PRODUCTIONS") or reader.peek("#END") or reader.peek("#DEFINITIONS")):    
            #idnum = reader.readInt()
            #reader.readUpTo(":")
            if reader.peek("'"):
                # Then the token was specified as a string like this:
                # '>=';
                reader.readUpTo("'")
                token = reader.readUpTo("'")[:-1].strip()
                previousId = newState()
                startStateId = previousId

                for c in token:
                    nextId = newState()
                    classSet = orderedcollections.OrderedSet([ord(c)])
                    if not (c in self.classes and self.classes[c] == classSet):
                        self.classes[c] = classSet
                    self.states[previousId].addTransition(c, nextId)
                    previousId = nextId

                self.states[nextId].setAccepting(idnum)
                startStates.append(startStateId)
                reader.readUpTo(";")
                self.tokens[idnum] = token
                idnum += 1
                if readingFirstToken and keywordsPresent:
                    raise Exception("First Token must be identifier token for matching keywords!")

            else:
                # The token was specified as a regular expression like this:
                # identifier = letter.(letter|digit)*;
                
                name = reader.readUpTo("=")[:-1].strip()
                self.tokens[idnum] = name
                if readingFirstToken:
                    self.firstTokenId = idnum
                    readingFirstToken = False
                    
                startStateId, stopStateId = evaluateRegExpression(reader)

                self.states[stopStateId].setAccepting(idnum)
                idnum += 1
                startStates.append(startStateId)
                        
                reader.readUpTo(";") 
                reader.skipComments()
                
         
        # Create a 0th State as the start state   
        startState = nfastate.NFAState(0)
        self.numStates += 1
        self.states[0] = startState
        
        for startId in startStates:
            self.states[0].addTransition(epsilon,startId)
            
        self.startStateId = 0
        
        reader.readUpTo("#END")
        
    def writeListing(self, outStream):
        
        outStream.write("The NFA CREATED FOR THE REGULAR EXPRESSIONS IS:\n\n")
        
        outStream.write("The start state is: " + str(self.startStateId) + "\n\n")
        
        outStream.write("STATE     ON CLASS     GO TO     ACCEPTS\n")
        outStream.write("-----     --------     -----     -------\n")
        
        for stateId in range(self.numStates):
            if self.states[stateId].isAccepting():
                acceptsId = self.states[stateId].getAcceptsTokenId()
                tokenName = self.tokens[acceptsId]
            else:
                tokenName = ""  
                
            outStream.write("%5d %34s\n"%(stateId,tokenName))
                
            for onClass in self.states[stateId].getTransitions(): 
                for toStateId in self.states[stateId].getTransitions()[onClass]:      
                    outStream.write("%18s     %5d\n"%(onClass,toStateId))
                
            outStream.write("\n")
            
class DFA:
    def __init__(self, classes=orderedcollections.OrderedMap(), states=orderedcollections.OrderedMap(), keywords = orderedcollections.OrderedMap(), tokens = orderedcollections.OrderedMap(), firstTokenId=-1):
        self.classes = orderedcollections.OrderedMap(classes)
        self.states = orderedcollections.OrderedMap(states)
        self.numStates = len(states)
        self.keywords = orderedcollections.OrderedMap(keywords)
        self.tokens = orderedcollections.OrderedMap(tokens)
        self.firstTokenId=firstTokenId
        
    def __repr__(self):
        return ("DFA(" + repr(self.classes) + "," + repr(self.states) + "," + repr(self.keywords) + "," + repr(self.tokens) + "," + repr(self.firstTokenId) + ")")
    
        
    def buildFromNFA(self,nfa):
        def newState():
            aState = state.State(self.numStates)
            self.states[self.numStates] = aState
            self.numStates+=1
            return self.numStates-1
        
        def getAcceptingTokenId(stateSet):
            for nfaStateId in stateSet:
                nfaState = nfa.states[nfaStateId]
                if nfaState.isAccepting():
                    return nfaState.getAcceptsTokenId()
                
            return None
            
            
        def EPSclosure(stateSet):
            closureSet = orderedcollections.OrderedSet(stateSet)
            stck = stack.Stack()
            for stateId in stateSet:
                stck.push(stateId)
                closureSet.add(stateId)
            
            while not stck.isEmpty():
                stateId = stck.pop()
                state = nfa.states[stateId]
                if epsilon in state.getTransitions():
                    toStates = state.getTransitions()[epsilon]
                    for toStateId in toStates:
                        if not toStateId in closureSet:
                            closureSet.add(toStateId)
                            stck.push(toStateId)
      
            return orderedcollections.OrderedFrozenSet(closureSet)
        
        def nfaTransTo(fromStates, onClass):
            toStates = orderedcollections.OrderedSet()
            for fromStateId in fromStates:
                if onClass in nfa.states[fromStateId].getTransitions():
                    toStates.update(nfa.states[fromStateId].getTransitions()[onClass])
                        
            return EPSclosure(toStates)
        
        def gatherClasses(states):
            classes = orderedcollections.OrderedSet()
            for stateId in states:
                for transClass in nfa.states[stateId].getTransitions():
                    if transClass != epsilon:
                        classes.add(transClass)
                        
            return classes  
        
        self.firstTokenId = nfa.firstTokenId        
        self.classes = nfa.classes
        self.keywords = nfa.keywords
        self.tokens = nfa.tokens
        
        self.startStateId = newState()
        self.stateMap = orderedcollections.OrderedMap()
        
        # This is the dfa state that maps to all the EPS-closure of the NFA start state.
        nfaSet = EPSclosure(orderedcollections.OrderedSet([0]))
        self.stateMap[self.startStateId] = nfaSet

        newDFAStates = orderedcollections.OrderedSet([self.startStateId])
        nfa2dfa = orderedcollections.OrderedMap()
        nfa2dfa[nfaSet] = self.startStateId
        
        tokenId = getAcceptingTokenId(nfaSet)
        if tokenId != None:
            self.states[self.startStateId].setAccepting(tokenId)
            
        
        while len(newDFAStates) > 0:
            fromDFAStateId = newDFAStates.pop()
            fromDFAState = self.states[fromDFAStateId]
            
            ## gather the transition alphabet from the NFA states
            nfaStates = self.stateMap[fromDFAStateId]
            classes = gatherClasses(nfaStates)
            
            for onclass in classes:
                nfaSet = nfaTransTo(nfaStates,onclass)

                if nfaSet in nfa2dfa:
                    # The DFA state already exists
                    dfaStateId = nfa2dfa[nfaSet]
                else:
                    # The DFA state does not exist so create it.
                    dfaStateId = newState()
                    self.stateMap[dfaStateId] = nfaSet
                    nfa2dfa[nfaSet] = dfaStateId
                    newDFAStates.add(dfaStateId)
                    tokenId = getAcceptingTokenId(nfaSet)
                    if tokenId != None:
                        self.states[dfaStateId].setAccepting(tokenId)
                        
                    
                fromDFAState.addTransition(onclass,dfaStateId)
                
        #print("Done Building DFA")
        
    def writeListing(self, outStream):
        
        outStream.write("The DFA CREATED FOR THE REGULAR EXPRESSIONS IS:\n\n")
        
        outStream.write("The start state is: " + str(self.startStateId) + "\n\n")
        
        outStream.write("STATE     ON CLASS     GO TO     ACCEPTS\n")
        outStream.write("-----     --------     -----     -------\n")
        
        for stateId in range(self.numStates):
            if self.states[stateId].isAccepting():
                acceptsId = self.states[stateId].getAcceptsTokenId()
                tokenName = self.tokens[acceptsId]
            else:
                tokenName = ""  
                
            outStream.write("%5d %34s\n"%(stateId,tokenName))
                
            trans = self.states[stateId].getTransitions()

            for onClass in trans:       
                outStream.write("%18s     %5d\n"%(onClass,trans[onClass]))
                
            outStream.write("\n")  
            
                
                
class MinimalDFA:
    def __init__(self):
        self.classes = orderedcollections.OrderedMap()
        self.states = orderedcollections.OrderedMap() 
        self.numStates = 0
        self.keywords = orderedcollections.OrderedMap()
        self.tokens = orderedcollections.OrderedMap()    

    def buildFromDFA(self,dfa):
        def newState():
            aState = state.State(self.numStates)
            self.states[self.numStates] = aState
            self.numStates+=1
            return self.numStates-1
        
        def transToMin(fromDFAStateId, onClass):
            state = dfa.states[fromDFAStateId]
            if not state.hasTransition(onClass):
                return -1
            
            return self.dfa2min[state.onClassGoTo(onClass)]
        
        def onClasses(minStateId):
            classes = orderedcollections.OrderedSet()
            
            for dfaStateId in self.stateMap[minStateId]:
                for onClass in dfa.states[dfaStateId].getTransitions():
                    classes.add(onClass)
                    
            return classes
        
        def finer(minStateId):
            #(*****************************************************************************)
            #(* Check each node in the given partition (the one passed as a parameter)    *)
            #(* with the first node in the partition. If a node is found that transitions *)
            #(* to a different partition than the first node on the same input make a new *)
            #(* partition and put all subsequent nodes that don't have similar transitions*)
            #(* to the first node into this new partition. Also, remove all nodes that    *)
            #(* have different transitions from the first partition.                      *)
            #(*****************************************************************************)   
            
            dfaStates = self.stateMap[minStateId]
            
            dfaStateList = list(dfaStates)
            
            dfaStateList.sort()
            
            firstDFAStateId = dfaStateList[0]
            firstDFAState = dfa.states[firstDFAStateId]
            newMinStateId = None
            
            for i in range(1,len(dfaStateList)):
                currentDFAStateId = dfaStateList[i]
                
                for onClass in onClasses(minStateId):
                    firstPartition = transToMin(firstDFAStateId,onClass)
                    currentPartition = transToMin(currentDFAStateId, onClass)
                    if firstPartition != currentPartition:
                        #print("found a difference on", onClass, "from state", minStateId)
                        if newMinStateId == None:
                            newMinStateId = newState()
                            self.stateMap[newMinStateId] = orderedcollections.OrderedSet()
                            
                        self.dfa2min[currentDFAStateId] = newMinStateId
                        self.stateMap[minStateId].discard(currentDFAStateId)
                        self.stateMap[newMinStateId].add(currentDFAStateId)
                        
                 
                 
            # return true if a change occurred.        
            return newMinStateId != None
                        

        def constructStates():
            for minStateId in self.states:
                minState = self.states[minStateId]
                
                for dfaStateId in self.stateMap[minStateId]:
                    if dfa.states[dfaStateId].isAccepting():
                        minState.setAccepting(dfa.states[dfaStateId].getAcceptsTokenId())
                    trans = dfa.states[dfaStateId].getTransitions()
                    for onClass in trans:
                        toDFAStateId = trans[onClass]
                        dfaState = dfa.states[toDFAStateId]
                        if not minState.hasTransition(onClass):
                            toStateId = self.dfa2min[toDFAStateId]
                            minState.addTransition(onClass,toStateId)
                            
                            
            self.startStateId = self.dfa2min[dfa.startStateId]
                            
        self.classes = dfa.classes
        self.keywords = dfa.keywords
        self.tokens = dfa.tokens
        
        startStateId = newState()
        self.stateMap = orderedcollections.OrderedMap()
        self.dfa2min = orderedcollections.OrderedMap()
        
        self.stateMap[startStateId] = orderedcollections.OrderedSet()
        
        # Build state sets. One with all
        # the non-final states in it, and one
        # for each accepting state of the dfa 
        # since we want separate accepting states
        # for all the tokens of the dfa. 
        
        for stateId in dfa.states:
            dfaState = dfa.states[stateId]
            
            if not dfaState.isAccepting():
                self.stateMap[startStateId].add(stateId)
                self.dfa2min[stateId] = startStateId                
            else:
                # Now we have to either add another partition (i.e. state) or 
                # find the accepting state that this dfa state belongs to. 
                
                found = False
                
                for minStateId in self.states:
                    minState = self.states[minStateId]
                    if minState.getAcceptsTokenId() == dfaState.getAcceptsTokenId():
                        self.stateMap[minStateId].add(stateId)
                        self.dfa2min[stateId] = minStateId
                        found = True
                        
                        
                if not found:
                    finalStateId = newState()
                    self.stateMap[finalStateId] = orderedcollections.OrderedSet([stateId])
                    self.dfa2min[stateId] = finalStateId
                    self.states[finalStateId].setAccepting(dfaState.getAcceptsTokenId())
                          
            
        # Now begins partitioning by finding distinguishable states
        
        changing = True
        
        while changing:
            changing = False
            
            for stateId in range(self.numStates):
                changed = finer(stateId)
                if changed:
                    changing = True
                    
        constructStates()

    def writeListing(self, outStream):
        
        outStream.write("The MINIMAL DFA CREATED FOR THE REGULAR EXPRESSIONS IS:\n\n")
        
        outStream.write("The start state is: " + str(self.startStateId) + "\n\n")
        
        outStream.write("STATE     ON CLASS     GO TO     ACCEPTS\n")
        outStream.write("-----     --------     -----     -------\n")
        
        for stateId in range(self.numStates):
            if self.states[stateId].isAccepting():
                acceptsId = self.states[stateId].getAcceptsTokenId()
                tokenName = self.tokens[acceptsId]
            else:
                tokenName = ""  
                
            outStream.write("%5d %34s\n"%(stateId,tokenName))
                
            trans = self.states[stateId].getTransitions()

            for onClass in trans:       
                outStream.write("%18s     %5d\n"%(onClass,trans[onClass]))
                
            outStream.write("\n")  
            
    def writeScanner(self, outStream, prefix, identifierTokenId):
        outStream.write("from genscanner import *\n")
        outStream.write("from state import *\n")
        
        commentTokenId = None
        outStream.write("\n#TOKEN Constants\n")
        val = "TokenToIDMap = {"
        val2 = "IDToTokenMap = {"
        for tokenId in self.tokens:
            if self.tokens[tokenId] == "comment":
                commentTokenId = tokenId
                
            val += "'" + self.tokens[tokenId] + "':" + str(tokenId) + ","
            val2 += str(tokenId) + ":'" + self.tokens[tokenId] + "',"
            
        val = val[:-1] + "}"
        val2 = val2[:-1] + "}"
        outStream.write(val+"\n")
        outStream.write(val2+"\n")
            
        outStream.write("\n#KEYWORD Constants\n")
        for keyword in self.keywords:
            outStream.write(keyword+"_keyword="+str(self.keywords[keyword])+"\n")
            
        outStream.write("\nclass " + prefix + "Scanner(Scanner):\n")
        outStream.write("\tdef __init__(self,instream):\n")
        if commentTokenId!=None:
            outStream.write("\t\tsuper().__init__(instream,0,"+repr(self.states) +","+repr(self.classes)+","+repr(self.keywords)+","+str(identifierTokenId)+",True,"+str(commentTokenId)+")\n\n")
        else:
            outStream.write("\t\tsuper().__init__(instream,0,"+repr(self.states) +","+repr(self.classes)+","+repr(self.keywords)+","+str(identifierTokenId)+",False)\n\n")
                
def main():  
    
    if len(sys.argv) != 2:
        print("usage: scangen inputfile")
        return
    
    filename = sys.argv[1]
    
    lst = filename.split(".")
    outputFilename = lst[0] + "scanner.py"
    instream = open(filename,'r')
    outstream = open(outputFilename,"w")
    
    nfa = NFA()
    nfa.buildMachine(instream)
    print(repr(nfa))
    nfa.writeListing(sys.stdout)
    
    dfa = DFA()
    dfa.buildFromNFA(nfa)
    dfa.writeListing(sys.stdout)
       
    minDFA = MinimalDFA()
    minDFA.buildFromDFA(dfa)
    minDFA.writeListing(sys.stdout)  
    minDFA.writeScanner(outstream, lst[0], nfa.getFirstTokenId())
        
    print("Scangen Completed.")      

if __name__ == "__main__":
    main()
    

        
    
            
    
                
            
        
                
            
            
