#ifndef function_h
#define function_h

#include "string"
#include "vector"
#include "saultree.h"

using namespace std;

/* ====== Variable ====== */
/** The variable class represents a variable in the SAUL language. This class
 * saves the value information, it's name and type. */
class Variable {
    private:
        int type;
        double value;
        string varName;

    public:
        Variable(int type, string varName);
        void setValue(double value);
        double getValue();
        string getName();
        int getType();
};

/* ====== Statements ======
 * Unary Statement */
/** The unary statement class represents a statement that only needs one
 * argument to work. This is a proxy to actions such as show, read and a
 * variable creation. */
class UnaryStatement {
    private:
        int action;
        Variable* var;

    public:
        UnaryStatement(int action, Variable* var);
        int getAction();
        Variable* getVariable();
};

/* Binary Statement */
/** The binary statement class represents a statement that needs one variable
 * and a vector of other arguments to work. This is a proxy to actions such as
 * calling a function and assigning a calculation to a variable. */
class BinaryStatement {
    private:
        vector<string> varsRight;
        int action;
        Variable* var;

    public:
        BinaryStatement(int action, Variable* varLeft, vector<string> varsRight);
        int getAction();
        Variable* getVariable();
        vector<string> getVarsRight();
};


/* ====== Function ====== */
/** The function class represents a SAUL function. This class saves all the
 * possible information surrounding one function such as the arguments needed to
 * run the function, the statements and their order. Lastly, they all have the
 * same instance of the saul calculator that is able to calculate mathematical
 * expressions following the grammar. */
class Function {
    private:
        // Attributes
        string nameFunc;
        vector<Variable*> args;
        vector<UnaryStatement*> unaryStatements;
        vector<BinaryStatement*> binaryStatements;
        vector<Function*> functions;
        vector<int> order;
        SaulCalculator* sc;
        string reserved [6] = { "*", "+", "-", "/", "(", ")" };

        // Functions
        bool isReserved(string word);
        bool isNum(string word);
        void executeUnaryStatement(int index);
        void executeBinaryStatement(int index);
        Variable* getVariable(string varName);

    public:
        Function(string nameFunc, vector<Variable*> args, SaulCalculator* sc);
        void addUnaryStatement(int action, Variable *varName);
        void addBinaryStatement(int action, Variable* var, vector<string> varsRight);
        void executeFunction(vector<double> args);
        void createVariable(Variable* var);
        string getName();
        void setFunctions(vector<Function*> functions);
};

/* ====== Constants ====== */
/* This constants represent different actions for statements. */
const int CREATE_VAR_INT = 0;
const int CREATE_VAR_FLOAT = 1;
const int SHOW_ACT = 2;
const int READ_ACT = 3;
const int CALL_FUNC = 4;
const int ASSIGN_VAR = 5;

#endif
