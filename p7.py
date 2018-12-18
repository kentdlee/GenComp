import p7scanner
import p7parser
import sys


def main():
    
    if (len(sys.argv)) != 2:
        print("usage: p7 filename")
        print("   p7 will interpret/compile the expression in the file named")
        print("   filename and print its result to standard output")
        return
    
    strm = open(sys.argv[1],"r")
    theScanner = p7scanner.p7Scanner(strm)
    theParser = p7parser.p7Parser()
    
    ast = theParser.parse(theScanner)
    print(ast)
    
if __name__ == "__main__":
    main()
