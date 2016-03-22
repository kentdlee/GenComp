import streamreader
import state
from orderedcollections import *
             
class Scanner:
    def __init__(self, instream = None, startStateId = None, states={}, classes={}, keywords = {}, identifierTokenId = -1, eatComments = False, commentTokenId = -1):
        # The use of dict below creates a copy of the default parameter because
        # only one copy of default parameters is created and if multiple scanner 
        # objects were created this would be a problem... for Python...
        self.states = dict(states)
        self.classes = dict(classes)
        self.startStateId = startStateId
        self.reader = streamreader.StreamReader(instream)
        self.keywords = dict(keywords)
        self.identiferTokenId = identifierTokenId
        self.eatComments = eatComments
        self.commentTokenId = commentTokenId
        for stateId in states:
            states[stateId].setClasses(classes)
  
    def getToken(self):        

        self.reader.skipWhiteSpace()
        
        stateId = self.startStateId
        
        lex = ""
        
        while True:
            ch = self.reader.readChar()
            
            theState = self.states[stateId]
            
            stateId = theState.onGoTo(ord(ch))
            
            if stateId == state.NoTransition:
                if theState.isAccepting():
                    self.reader.unreadChar(ch)
                    tokenId = theState.getAcceptsTokenId()
                    
                    if self.eatComments and tokenId == self.commentTokenId:
                        stateId = self.startStateId
                        self.reader.skipWhiteSpace()
                        lex = ""
                    elif tokenId == self.identiferTokenId and lex in self.keywords:
                        tokenId = self.keywords[lex]
                        return (tokenId, lex)
                    else:
                        return (tokenId, lex)
                else:
                    raise Exception("Bad Token '"+lex+ch+"' found at line " + str(self.reader.getLineNumber()) + " and column " + str(self.reader.getColNumber()) + ".")
                
            else:
                lex += ch

