import postfixscanner
import postfixparser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: postfix filename")
        print("   postfix will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = postfixscanner.postfixScanner(strm)
    theParser = postfixparser.postfixParser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
