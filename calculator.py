import calcscanner
import calcparser
import sys


def main():
    
    strm = sys.stdin
    theScanner = calcscanner.calcScanner(strm)
    theParser = calcparser.calcParser()
    
    ast = theParser.parse(theScanner)
    
if __name__ == "__main__":
    main()
