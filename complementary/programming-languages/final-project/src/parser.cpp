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
#include "parser.h"
#include "lexer.h"
#include "token.h"

using namespace std;

/** The parser is constructed only using the input file that it is going to be
 * parsed with the SAUL grammar. */
Parser::Parser(string strFileName) {
	fstream prueba;
	prueba.exceptions( std::fstream::failbit | std::fstream::badbit );

	// File finding
	try {
		prueba.open(strFileName, fstream::in);
		prueba.close();
	}
	catch (fstream::failure e) {
		cout << "SAUL no pudo encontrar tu archivo. "
			 << "Quizá no soy el único amateur... Archivo: "
			 << strFileName << endl;
		exit(3);
	}

	// Lexer creation
	try {
		lexer = new Lexer(strFileName);
		token = lexer->nextToken();
	}
	catch (fstream::failure e) {
		cout << "¡Changos! Dañaste el archivo... Archivo: " << strFileName
			 << endl;
		exit(3);
	}
}

/** Destructor */
Parser::~Parser() {
	delete token;
	delete lexer;
}

/** Check if the current token is the same as expected, by the SAUL grammar. */
void Parser::recognize(int expected) {
	// Succesful case
	if (token->getCode() == expected) {
		token = lexer -> nextToken();
	}
	else {
		// Unexpected error
		cout << "SAUL reporta un error.\n"
		     << "Esperado: " << lexer->getTokenText(expected)
			 << "\nEncontrado: " << lexer->getTokenText(token->getCode())
			 << "\nLínea " << lexer -> getLineNumber()
			 << endl;
		exit(2);
	}
}


/** Program parsing, defined by the SAUL grammar. */
void Parser::program() {
	recognize(PROGRAM);
	funDefinitionList();
	recognize(ENDPROGRAM);
}

/** Function definitions parsing. In this, each of the functions is parsed
 * individually. */
void Parser::funDefinitionList() {
	if(token->getCode() == DEF) {
		funDefinition();
		funDefinitionList();
	}
}

/** This function parses only one function in the SAUL grammar. */
void Parser::funDefinition() {
	// Header for function
	recognize(DEF);
	recognize(VARIABLE);
	recognize(LPAREN);
	varDefList();
	recognize(RPAREN);

	// Variable definitions
	varDefList();

	// Statements
	statementList();

	// End function definition
	recognize(ENDDEF);
}

/** Define a list of variables, each one with it's respective type and name as
 * the ones avaialble in SAUL. */
void Parser::varDefList() {
	if (token -> getCode() == INT) {
		recognize(INT);
		recognize(VARIABLE);
		varDefList();
	}
	else if (token -> getCode() == FLOAT) {
		recognize(FLOAT);
		recognize(VARIABLE);
		varDefList();
	}
}


/** Parses the statement list given by the SAUL grammar. */
void Parser::statementList() {
	if (token -> getCode() == READ || token -> getCode() == PRINT ||
		token -> getCode() == CALL || token -> getCode() == VARIABLE) {
		statement();
		statementList();
	}
}

/** Parses a single statement, given by a read function, a print function, a
 * calling to another function and an assignment to a variable. */
void Parser::statement() {
	switch (token -> getCode()) {
		case READ:
			recognize(READ);
			recognize(VARIABLE);
			break;
		case PRINT:
			recognize(PRINT);
			recognizeVariableConstant();
			break;
		case CALL:
			recognize(CALL);
			recognize(VARIABLE);
			recognize(LPAREN);
			variableList();
			recognize(RPAREN);
			break;
		case VARIABLE:
			recognize(VARIABLE);
			recognize(ASSIGN);
			recognizeMathExp();
			break;
		default:
			break;
	}
}

void Parser::recognizeVariableConstant() {
	if (token -> getCode() == VARIABLE)
		recognize(VARIABLE);
	else if (token -> getCode() == CONSTANT)
		recognize(CONSTANT);
}

/** This function recognizes a correct mathematical expression given by the SAUL
 * grammar. */
void Parser::recognizeMathExp() {
	bool foundPrevious = false;

	if (token -> getCode() == VARIABLE || token -> getCode() == CONSTANT) {
		// Start variable
		recognizeVariableConstant();
		foundPrevious = true;

	}
	else if (token -> getCode() == LPAREN) {
		// Parenthesis equation
		recognize(LPAREN);
		recognizeMathExp();
		recognize(RPAREN);
		foundPrevious = true;
	}

	// Operation with previous math equation
	if (foundPrevious && (token -> getCode() == SUM ||
						  token -> getCode() == SUB ||
						  token -> getCode() == DIV ||
						  token -> getCode() == MULT)) {
		recognize(token -> getCode());
		recognizeMathExp();
	}
}

/** Recognizes a list of variables with no type. */
void Parser::variableList() {
	if (token -> getCode() == VARIABLE || token -> getCode() == CONSTANT) {
		recognizeVariableConstant();
		variableList();
	}
}
