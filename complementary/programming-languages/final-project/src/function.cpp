#include "function.h"

#include "cmath"
#include "iostream"
#include "lexer.h"
#include "string"
#include "vector"

using namespace std;

/* ====== Variable ====== */
/** Constructor for a Variable. */
Variable::Variable(int type, string varName) {
    this -> type = type;
    this -> varName = varName;
}

/** This function sets the value for a variable. If the type is integer and a
 * value that is not an integer is passed the function exits with an error. */
void Variable::setValue(double value) {
    if (type == INT && modf(value, &value) == 0.0)
        this -> value = value;
    else if (type == FLOAT)
        this -> value = value;
    else {
        cout << "Se le asignó un real a una variable entera." << endl;
        exit(3);
    }
}

/* Getters */
double Variable::getValue() {
    return this -> value;
}

string Variable::getName() {
    return this -> varName;
}

int Variable::getType() {
    return this -> type;
}

/* ====== Unary Statement ====== */
/** Constructor for unary statement. */
UnaryStatement::UnaryStatement(int action, Variable* var) {
    this -> action = action;
    this -> var = var;
}

/* Getters */
int UnaryStatement::getAction() {
    return action;
}

Variable* UnaryStatement::getVariable() {
    return var;
}

/* ====== Binary Statement ====== */
/** Constructor for binary statement. */
BinaryStatement::BinaryStatement(int action, Variable* varLeft,
                                 vector<string> varRight) {
    this -> action = action;
    this -> var = varLeft;
    this -> varsRight = varRight;
}

/* Getters */
int BinaryStatement::getAction() {
    return this -> action;
}

Variable* BinaryStatement::getVariable() {
    return this -> var;
}

vector<string> BinaryStatement::getVarsRight() {
    return this -> varsRight;
}

/* ====== Function ====== */
/** Constructor for the function class. */
Function::Function(string nameFunc, vector<Variable*> args, SaulCalculator* sc) {
    this -> nameFunc = nameFunc;
    this -> args = args;
    this -> sc = sc;
}

/** This methods add a binary statement to the list of instructions. */
void Function::addBinaryStatement(int action, Variable* var,
                                  vector<string> varsRight) {
    this -> binaryStatements.push_back(new BinaryStatement (action, var, varsRight));
    order.push_back(unaryStatements.size() + binaryStatements.size() - 1);
}

/** This methods add a unary statement to the list of instructions. At adding a
 * unary statement it updates the order of the binary statements as the index
 * for running the binary statements depends on the size of the unary statements. */
void Function::addUnaryStatement(int action, Variable *var) {
    for (vector<int>::iterator it=order.begin(); it != order.end(); ++it) {
        if (*it >= unaryStatements.size())
            *it += 1;
    }
    this -> unaryStatements.push_back(new UnaryStatement (action, var));
    order.push_back(unaryStatements.size() - 1);
}

/** This method executes the instructions of a function with the args passed. */
void Function::executeFunction(vector<double> args) {
    // Check for errors
    if (args.size() != this -> args.size()) {
        cout << "Pusiste un número diferente de argumentos en la funcion "
             << this -> nameFunc << endl;
        exit(3);
    }

    // Set values
    for (int i = 0; i < args.size(); i++) {
        this -> args[i] -> setValue(args[i]);
    }

    // Run function
    for (int index : order) {
        if (index >= unaryStatements.size()) {
            index -= unaryStatements.size();
            this -> executeBinaryStatement(index);
            continue;
        }
        this -> executeUnaryStatement(index);
    }
}

/** This method executes the unary statement of the respective index in the
 * unary statement instructions list. */
void Function::executeUnaryStatement(int index) {
    UnaryStatement* statement = this -> unaryStatements[index];
    switch (statement -> getAction()) {
        case CREATE_VAR_FLOAT:
            createVariable(statement -> getVariable());
            break;
        case CREATE_VAR_INT:
            createVariable(statement -> getVariable());
            break;
        case SHOW_ACT: {
            Variable* var = getVariable(statement -> getVariable() -> getName());
            cout << var -> getName() << " = " << var -> getValue() << endl;
            break;
        }
        case READ_ACT: {
            Variable* var = getVariable(statement -> getVariable() -> getName());
            double value;
            cout << var -> getName() << " : ";
            cin >> value;
            var -> setValue(value);
            break;
        }
        default:
            break;
    }
}

/** This method executes the binary statement of the respective index in the
 * binary statement instructions list. */
void Function::executeBinaryStatement(int index) {
    BinaryStatement* statement = this -> binaryStatements[index];
    switch (statement -> getAction()) {
        case ASSIGN_VAR: {
            string varName = statement -> getVariable() -> getName();

            // Substitute variables
            vector<string> varsRight = statement -> getVarsRight();
            vector<string> numEq;
            for (int i = 0; i < varsRight.size(); i++) {
                if (!isReserved(varsRight[i]) && !isNum(varsRight[i])) {
                    double value = getVariable(varsRight[i]) -> getValue();
                    string valueStr = to_string(value);
                    numEq.push_back(valueStr);
                    continue;
                }
                numEq.push_back(varsRight[i]);
            }

            // Calculate expression
            Variable* var = getVariable(varName);
            double value = sc -> calculateExpression(numEq);

            // Assign
            var -> setValue(value);
            break;
        }
        case CALL_FUNC: {
            string funcName = statement -> getVariable() -> getName();
            // Search for function
            for (Function* func : functions) {
                if (func -> getName() == funcName) {
                    vector<string> varNames = statement -> getVarsRight();
                    vector<double> args;

                    // Replace arguments
                    for (string name : varNames) {
                        if (!isNum(name))
                            args.push_back(getVariable(name) -> getValue());
                        else
                            args.push_back(stod(name));
                    }

                    // Execute function
                    func -> executeFunction(args);
                    return;
                }
            }
            cout << "La función llamada " << funcName << " no existe." << endl;
            exit(3);
            break;
        }
        default:
            break;
    }
}

/** This function creates a variable. If a variable with the same type and name
 * already exists, the value is reseted to 0. If the variables does not exists,
 * it is created locally. Lastly if the name is the same but the type is changed
 * then the function exits with an error. */
void Function::createVariable(Variable* var) {
    for (int i = 0; i < args.size(); i++) {
        if (args[i] -> getName() == var -> getName()) {
            if (args[i] -> getType() == var -> getType()) {
                cout << "Advertencia: Hay pérdida de información, dado que se"
                     << " redefinió una variable. SAUL está decepcionado." << endl;
                args[i] -> setValue(0);
                return;
            }
            else {
                cout << "Error: se intentó cambiar el tipo de la variable "
                    << args[i] -> getName() << endl;
                exit(3);
            }
        }
    }

    args.push_back(var);
}

/** This function searches for a local variable. If not found, an error is done. */
Variable* Function::getVariable(string varName) {
    for (int i = 0; i < args.size(); i++) {
        if (args[i] -> getName() == varName)
            return args[i];
    }

    cout << "Se intentó acceder la variable " << varName
         << ". Esta no está definida." << endl;
    exit(3);
    return new Variable (-1, "");
}

/** Get the name of a function. */
string Function::getName() {
    return this -> nameFunc;
}

/** Set a vector to all the other functions. */
void Function::setFunctions(vector<Function*> functions) {
    this -> functions = functions;
}

/** It returns true if a word is a reserved word in a mathematical
 * expression. */
bool Function::isReserved(string word) {
    for (string resWord : reserved) {
        if (word == resWord)
            return true;
    }
    return false;
}

/** It returns true if a string is a possible variable name is a number. This
 * takes advantage of the fact the variables can not start with a number. */
bool Function::isNum(string word) {
    return '0' <= word[0] && word[0] <= '9';
}
