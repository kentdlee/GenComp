from lr0state import *
import stack
import streamreader
import io
import sys

class Parser:
    def __init__(self,states,tnts):
        self.states = states
        self.tnts = tnts
        for stateId in states:
            theState = states[stateId]
            theState.tnts = tnts
            for item in theState.items:
                item.tnts = tnts
            #print(theState)
            

    def buildReturnValue(self,item,prodStack):
        # We found an item to reduce by.
        prodNames = {} # this is a map from return value names to locations with rhs
        tntCount = {}
        rhsVals = {} # this is a map from index location of rhs to value from the stack.
        
        # this loop builds a map from names of rhs terminals or nonterminals to
        # their index value for the rhs
        for i in range(len(item.production.rhs)):
            tntId = item.production.rhs[i]
            tnt = self.tnts[tntId]
            if not tnt in tntCount:
                tntCount[tnt] = 1
                prodNames[tnt] = i
                prodNames[tnt+"1"] = i
            else:
                numVal = tntCount[tnt]+1
                tntCount[tnt] = numVal
                prodNames[tnt+str(numVal)]=i

        
        # this loop builds a map from index value of rhs location to 
        # the actual value popped from the pda stack.
        for i in range(len(item.production.rhs)-1,-1,-1):
            stateId, val = prodStack.pop()
            rhsVals[i] = val
            
        returnValue = ""
        rvStrm  = streamreader.StreamReader(io.StringIO(item.production.returnValue))
        
        # Here we iterate through the parts of the return value replacing any
        # non-terminal token with the actual value popped from the stack
        # used in parsing. This builds the actual return value for the expression
        # being parsed. 

        token = rvStrm.getToken()
        
        while not rvStrm.eof():
            if token in prodNames:
                returnValue += rhsVals[prodNames[token]]
            else:
                returnValue += token
                
            token = rvStrm.getToken()
            
        # Here we call the overridden eval method to evaluate
        # the return value string in the context of the parser's
        # back end module. This is because each parser instance
        # inherits from this class to define its own parser 
        # and backend code. 
        
        val = repr(self.eval(returnValue))
        return val


    # This algorithm comes from page 218, Algorithm 4.7 from Aho,
    # Sethi, and Ullman. 
    # The modification from this algorithm has the stack a stack of 
    # tuples of (stateId, val) where val is the return value
    # for a terminal or nonterminal.
    def parse(self, theScanner):
            
        prodStack = stack.Stack()
        
        # push the start state and return value
        prodStack.push((0,None))
        
        done = False
        needToken = True
        
        while True:
            # Peek at the top of the stack to get the stateId and return value.
            stateId, topVal = prodStack.peek()
            theState = self.states[stateId]
            
            # Get a token if needed.
            if needToken:
                tokenId, lex = theScanner.getToken()
                needToken = False
                
            # Do a shift operation if there is a transition on the tokenId. If we also had the same
            # tokenId in a lookahead set we would have a shift/reduce conflict, but we'll always shift
            # anyway in that case so don't worry about detecting shift/reduce conflicts. 
            if theState.hasTransition(tokenId):
                stateId = theState.onClassGoTo(tokenId)
                prodStack.push((stateId,lex))
                needToken = True
            else:
                # we look in the items of the state for an item that would
                # work to reduce by. If more than one item is found then we have a 
                # reduce/reduce conflict. 
                theMatchingItem = None
                foundMatch = False                
                for item in theState.items:
                    # for each item in the LR0 State
                    if theState.isAccepting() or (item.dotIndex == len(item.production.rhs)) and (tokenId in item.la):  
                        # only one match should be found. Otherwise there would be a 
                        # reduce/reduce comflict. 
                        if foundMatch:
                            sys.stderr.write("Reduce/reduce conflict in the parser between productions:\n")
                            sys.stderr.write(str(item.production)+"\n")
                            sys.stderr.write(str(theMatchingItem.production)+"\n")
                            raise Exception("Reduce/reduce conflict in the parser.")
                        theMatchingItem = item
                        foundMatch = True

                # If an item to reduce by is found then call buildReturnValue which will build the return
                # value (e.g. usually an AST) for the reduction. 
                # NOTE: buildReturnValue pops off the correct number of values from the stack, but does not
                # push on the new state found by following the transition on the LHS of the chosen item.     
                if foundMatch:
                    val = self.buildReturnValue(theMatchingItem,prodStack)
                    lhsId = theMatchingItem.production.lhsId

                    
                    if theState.isAccepting():
                        return val
                    
                    stateId, topVal = prodStack.peek()
                    
                    nextStateId = self.states[stateId].onClassGoTo(lhsId)
                    
                    prodStack.push((nextStateId, val))
                
                    
                # if no item was found then there is a problem
                else:
                    sys.stderr.write("No Transition Found\n")
                    sys.stderr.write("\nState is " + str(stateId) + "\n\n")
                    sys.stderr.write("Stack Contents\n")
                    sys.stderr.write("==============\n\n")
                    sys.stderr.write(str(prodStack)+"\n\n\n")
                    sys.stderr.write("Next Input Symbol is "+lex+" with tokenId of "+str(tokenId)+"\n\n")
                    raise Exception("No transition on state!")
                    
                    
                        
                            
                            
                        
                             
                                
                                
                            
                        
                
                
            
            
            
