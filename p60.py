import p60scanner
import p60parser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: p60 filename")
        print("   p60 will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = p60scanner.p60Scanner(strm)
    theParser = p60parser.p60Parser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
