import state
import io
import streamreader

class FiniteStateMachine:
    def __init__(self, states, startStateId, classes):
        self.states = states
        self.startStateId = startStateId
        self.classes = classes
        
        for stateId in self.states:
            self.states[stateId].setClasses(classes)
            
        
    def accepts(self, strm):
        stateId = self.startStateId
        
        while True:
            theState = self.states[stateId]
            print("state is", stateId)
            on = strm.readChar()
            
            if strm.eof():
                return theState.isAccepting()
            
            stateId = theState.onGoTo(on)

            
            if stateId == state.NoTransition:
                return False

            
def main():
    
    q0 = state.State(0)
    q1 = state.State(1,1)
    q2 = state.State(2)
    classes = {"zero":frozenset("0"), "one":frozenset("1")}
    
    q0.addTransition("zero", 0)
    q0.addTransition("one", 1)
    q1.addTransition("zero", 0)
    q1.addTransition("one",2)
    q2.addTransition("zero",2)
    q2.addTransition("one",1)
    
    dfa = FiniteStateMachine({0:q0, 1:q1, 2:q2}, 0, classes)
    
    done = False
    
    while not done:
        s = input("Please enter a string of zeros and ones: ").strip()
        if len(s) == 0:
            done = True
        else:
            strm = streamreader.StreamReader(io.StringIO(s))
            if dfa.accepts(strm):
                print("The string is accepted by the finite state machine.")
            else:
                print("The string is not accepted.")
                
    print("Program Completed.")
                
if __name__=="__main__":
    main()
            
        
    
    
    
    