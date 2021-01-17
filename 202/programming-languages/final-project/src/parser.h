#ifndef parser_h
#define parser_h

#include <string>

#include "token.h"
#include "lexer.h"

using namespace std;

/* ====== Parser ====== */
/** The parser checks if the code has compliance with the SAUL grammar. The
 * parser verifies the grammar using the Lexer's output and not directly from
 * the file. */
class Parser {
    private:
        Token* token;
        Lexer* lexer;
        void recognize(int expected);
        void recognizeMathExp();

    public:
        Parser(string strFileName);
        virtual ~Parser();
        void program();
        void funDefinitionList();
        void funDefinition();
        void varDefList();
        void varDef();
        void statementList();
        void statement();
        void variableList();
        void recognizeVariableConstant();
};

#endif
