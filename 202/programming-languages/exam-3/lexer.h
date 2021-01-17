#ifndef lexer_h
#define lexer_h

#include <fstream>
#include <sstream>
#include <string>
#include "token.h"
#include <vector>

using namespace std;

/* ====== Lexer ====== */
/** The lexer is encharged of processing the string program and processing it
 * into a higher structure for the parser to compile. This is done in order to
 * simplify the SAUL parsing process. */
class Lexer {
    private:
        int lineNumber;
        vector<Token> table;
        fstream fileScanner;
        string lineScanner;
        bool validVariableName(string text);
        bool validConstant(string text, int code);

    public:
        Lexer(string strFileName);
        virtual ~Lexer();
        string nextText();
        Token* nextToken();
        string getTokenText(int code);
        int getLineNumber();
};

/* ====== Constants ====== */
const int PROGRAM = 1;
const int ENDPROGRAM = 2;
const int DEF = 3;
const int ENDDEF = 4;
const int CONSTANT = 5;
const int VARIABLE = 8;
const int ASSIGN = 11;
const int LPAREN = 12;
const int RPAREN = 13;
const int INT = 14;
const int READ = 15;
const int PRINT = 16;
const int CALL = 17;
const int FLOAT = 18;
const int SUM = 19;
const int DIV = 20;
const int SUB = 21;
const int MULT = 22;
const int INVALIDTOKEN = 98;
const int TEOF = 99;

#endif
