#ifndef saulrunner_h
#define saulrunner_h

#include "map"
#include "string"
#include "vector"
#include "function.h"
#include "token.h"
#include "lexer.h"
#include "saultree.h"

using namespace std;

/* ====== SaulRunner ====== */
/** The saul runner class runs a correctly structured file using the SAUL
 * grammar. The execution is done through the main function with no
 * arguments. */
class SaulRunner {
    private:
        // Attributes
        Lexer* lexer;
        Token* token;
        SaulCalculator* sc;
        vector<Function*> functions;
        Function* mainFunc;

        // Functions
        void recognize(int expected);
        vector<string> recognizeMathExp();
        void executeProgram();
        void funDefinitionList();
        void funDefinition();
        vector<Variable*> varDefList();
        void varDefStatement(Function* func);
        void varDef();
        void statementList(Function* func);
        void statement(Function* func);
        void variableList(vector<string>& varsRight);

    public:
        // Main Functions
        SaulRunner(string strFileName);
        void runProgram();
};

#endif
