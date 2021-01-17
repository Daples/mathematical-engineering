/** Parser for the SAUL grammar.
 *
 * @author Helmuth Trefftz
 * @author Jose Luis Montoya
 * @author Juan Sebastián Cárdenas
 * @author Manuela Gallego Gómez
 */
#include <string>
#include <iostream>
#include <fstream>
#include "saulrunner.h"
#include "lexer.h"

using namespace std;

/** Constructor for the SaulRunner. It recieves the name file that the structure
 * will be compiled from. It uses the lexer meta-language to process the
 * file. */
SaulRunner::SaulRunner(string strFileName) {
  lexer = new Lexer(strFileName);
  token = lexer -> nextToken();
  sc = new SaulCalculator();
}

/** Move to next token. The expected variable is only to used to improve
 * code readibility. */
void SaulRunner::recognize(int expected) {
  token = lexer -> nextToken();
}

/** This function reads all the functions and searches for the main function.
 * Then it executes the main. It exits with an error if a main function does not
 * exist. */
void SaulRunner::runProgram() {
  recognize(PROGRAM);
  funDefinitionList();
  recognize(ENDPROGRAM);

  // Parsed all file correctly
  for (Function* func : functions) {
    func -> setFunctions(functions);
  }

  if (mainFunc) executeProgram();
  else {
    cout << "No hay función principal para ejecutar." << endl;
    exit(3);
  }
}

/** This function runs the main function. This was separated from the method
 * above in order to, in a future, implement arguments to the main. */
void SaulRunner::executeProgram() {
  vector<double> args;
  this -> mainFunc -> executeFunction(args);
}

/** This function saves all functions in a file. */
void SaulRunner::funDefinitionList() {
  if(token->getCode() == DEF) {
    funDefinition();
    funDefinitionList();
  }
}

/** This function extracts all the important information of a function and
 * detects if a main function is defined in the file. Furthermore, it saves all
 * the functions instructions in an assembly-like manner to facilitate
 * processing. */
void SaulRunner::funDefinition() {
  // Header for function
  recognize(DEF);

  // Name function
  string nameFunction = token -> getText();
  recognize(VARIABLE);

  // Read arguments
  recognize(LPAREN);
  vector<Variable*> args = varDefList();
  recognize(RPAREN);

  // Add function
  Function* func = new Function (nameFunction, args, sc);
  if (nameFunction == "principal")
    mainFunc = func;
  functions.push_back(func);

  // Variable definitions
  varDefStatement(func);

  // Statements
  statementList(func);

  // End function definition
  recognize(ENDDEF);
}

/** This function saves the name and type of all the arguments of a function. It
 * returns a vector with the arguments. */
vector<Variable*> SaulRunner::varDefList() {
  vector<Variable*> args;
  while (token -> getCode() == INT || token -> getCode() == FLOAT) {
    // Recognize type
    int type = token -> getCode();
    recognize(-1);

    // Save variable
    string varName = token -> getText();
    recognize(VARIABLE);
    args.push_back(new Variable (type, varName));
  }
  return args;
}

/** This function creates the statements to create integer or float variables in
 * a function instructions list. */
void SaulRunner::varDefStatement(Function* func) {
  if (token -> getCode() == INT || token -> getCode() == FLOAT) {
    // Recognize type
    int type = token -> getCode();
    recognize(-1);

    // Save variable
    string varName = token -> getText();
    Variable* var = new Variable (type, varName);
    recognize(VARIABLE);

    int action = token -> getCode() == INT ? CREATE_VAR_INT : CREATE_VAR_FLOAT;
    func -> addUnaryStatement(action, var);

    // Read next
    varDefStatement(func);
  }
}

/** This function processes all the other possible instructions for a given
 * function. */
void SaulRunner::statementList(Function* func) {
  if (token -> getCode() == READ || token -> getCode() == PRINT ||
      token -> getCode() == CALL || token -> getCode() == VARIABLE) {
    statement(func);
    statementList(func);
  }
}

/** This function saves all the possible instructions in a given function and
 * extracts the important information needed to run each line. */
void SaulRunner::statement(Function* func) {
  switch (token -> getCode()) {
    case READ: {
      recognize(READ);

      // Variable name to read
      string varName = token -> getText();
      recognize(VARIABLE);

      Variable* var = new Variable (-1, varName);
      func -> addUnaryStatement(READ_ACT, var);
      break;
    }
    case PRINT: {
      recognize(PRINT);

      // Variable name to show
      string varName = token -> getText();
      recognize(VARIABLE);

      Variable* var = new Variable (-1, varName);
      func -> addUnaryStatement(SHOW_ACT, var);
      break;
    }
    case CALL: {
      recognize(CALL);

      // Name of function
      string varName = token -> getText();
      recognize(VARIABLE);

      Variable* varLeft = new Variable(-1, varName);
      recognize(LPAREN);

      // Arguments list
      vector<string> varsRight;
      variableList(varsRight);

      func -> addBinaryStatement(CALL_FUNC, varLeft, varsRight);
      recognize(RPAREN);
      break;
    }
    case VARIABLE: {
      // Variable name to assign expression
      string varName = token -> getText();
      recognize(VARIABLE);
      recognize(ASSIGN);
      Variable* var = new Variable(-1, varName);

      // Mathematical expression
      vector<string> varsRight = recognizeMathExp();

      func -> addBinaryStatement(ASSIGN_VAR, var, varsRight);
      break;
    }
    default:
      break;
  }
}

/** This function saves all the variable names passed to a function as arguments
 * and saves the names in the vector varsRight. Furthermore, as passing
 * constants is also possible this also saves those constants. */
void SaulRunner::variableList(vector<string>& varsRight) {
  if (token -> getCode() == VARIABLE || token -> getCode() == CONSTANT) {
    string text = token -> getText();
    varsRight.push_back(text);

    recognize(-1);
    variableList(varsRight);
  }
}

/** This function saves each character of a mathematical equation in a vector of
 * strings and returns it. */
vector<string> SaulRunner::recognizeMathExp() {
  vector<string> varsRight;
  while (true) {
    if (token -> getCode() == VARIABLE || token -> getCode() == CONSTANT
        || token -> getCode() == LPAREN || token -> getCode() == RPAREN ||
        token -> getCode() == SUM || token -> getCode() == SUB ||
        token -> getCode() == MULT || token -> getCode() == DIV) {
      varsRight.push_back(token -> getText());
      recognize(-1);
      continue;
    }
    break;
  }
  return varsRight;
}
