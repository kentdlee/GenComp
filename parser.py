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
            
    # This algorithm comes from page 218, Algorithm 4.7 from Aho,
    # Sethi, and Ullman. 
    # The modification from this algorithm has the stack a stack of 
    # triples of (stateId, tntId, val) where val is the return value
    # for a terminal or nonterminal.
    def parse(self, theScanner):
            
        prodStack = stack.Stack()
        
        # push the start state and return value
        prodStack.push((0,None))
        
        done = False
        needToken = True
        
        while True:
            stateId, topVal = prodStack.peek()
            theState = self.states[stateId]
            
            if needToken:
                tokenId, lex = theScanner.getToken()
                needToken = False
                
            if theState.hasTransition(tokenId):
                stateId = theState.onClassGoTo(tokenId)
                prodStack.push((stateId,lex))
                needToken = True
            else:
                # we look in the items of the state for an item that would
                # work to reduce by.
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

                
                #theMatchingItem = None
                #foundMatch = False
                #for item in theState.items:
                    ## for each item in the LR0 State
                    #if (item.dotIndex == len(item.production.rhs)) and (tokenId in item.la):  
                        #theMatchingItem = item
                        #foundMatch = True
                        
                #if not foundMatch:
                    #for item in theState.items:
                        #if (item.dotIndex == len(item.production.rhs)):  
                            #theMatchingItem = item
                            #foundMatch = True
                            
                if foundMatch:
                    item = theMatchingItem
                    lhsId = item.production.lhsId
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
                    
                    token = rvStrm.getToken()
                    
                    while not rvStrm.eof():
                        if token in prodNames:
                            returnValue += rhsVals[prodNames[token]]
                        else:
                            returnValue += token
                            
                        token = rvStrm.getToken()
                        
                    # Here we call the overridden eval method to evaluate
                    # the return value string in the context of the parser's
                    # back end module. 
                    val = self.eval(returnValue)
                    
                    if theState.isAccepting():
                        return val
                    
                    stateId, topVal = prodStack.peek()
                    
                    nextStateId = self.states[stateId].onClassGoTo(lhsId)
                    
                    prodStack.push((nextStateId, repr(val)))
                
                    
                # if no item was found then there is a problem
                else:
                    sys.stderr.write("No Transition Found\n")
                    sys.stderr.write("\nState is " + str(stateId) + "\n\n")
                    sys.stderr.write("Stack Contents\n")
                    sys.stderr.write("==============\n\n")
                    sys.stderr.write(str(prodStack)+"\n\n\n")
                    sys.stderr.write("Next Input Symbol is "+lex+" with tokenId of "+str(tokenId)+"\n\n")
                    raise Exception("No transition on state!")
                    
                    
                        
                            
                            
                        
                             
                                
                                
                            
                        
                
                
            
            
            
