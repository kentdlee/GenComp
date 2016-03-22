import jpythonscanner

# This is a test program for the scangen generated 
# scanner for the JPython language.

def main():
    print("This is testscanner.py testing a scangen generated automaton.")
    strm = open("sample.jpy")
    
    theScanner = jpythonscanner.jpythonScanner(strm)
    
    done = False
    while not done:
        (ident,lex) = theScanner.getToken()
        print(ident,lex)
        if ident == jpythonscanner.TokenToIDMap["endoffile"]:
            done = True
        
    #for stateId in theScanner.states:
    #    print(theScanner.states[stateId])
    

if __name__ == "__main__":
    main()
