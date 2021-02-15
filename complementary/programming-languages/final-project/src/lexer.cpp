/**
 * Very simple Lexer, built on the Java Scanner. Limitation: all the symbols
 * have to be separted with spaces in the source file. This lexer is adapted to
 * fit the rules dictated by the SAUL programming language.
 *
 * @author Helmuth Trefftz
 * @author Juan Sebatián Cárdenas
 * @author Manuela Gallego Gómez
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "lexer.h"

using namespace std;

/** The lexer is constructed given an initial file that will be compiled using
 * the SAUL grammar. */
Lexer::Lexer(string strFileName) {
	fileScanner.open(strFileName, fstream::in);

	// Program tokens
	table.push_back(Token(PROGRAM, "codigo"));
	table.push_back(Token(ENDPROGRAM, "fincodigo"));

	// Function tokens
	table.push_back(Token(DEF, "funcion"));
	table.push_back(Token(ENDDEF, "finfuncion"));

	// Type of numbers
	table.push_back(Token(INT, "entero"));
	table.push_back(Token(FLOAT, "real"));

	// Default functions
	table.push_back(Token(READ, "leer"));
	table.push_back(Token(PRINT, "mostrar"));
	table.push_back(Token(CALL, "llamar"));

	// Operations
	table.push_back(Token(DIV, "/"));
	table.push_back(Token(SUB, "-"));
	table.push_back(Token(MULT, "*"));
	table.push_back(Token(SUM, "+"));

	// Other tokens
	table.push_back(Token(VARIABLE, "variable"));
	table.push_back(Token(ASSIGN, "="));
	table.push_back(Token(LPAREN, "("));
	table.push_back(Token(RPAREN, ")"));
	table.push_back(Token(TEOF, "TEOF"));

	lineNumber = 1;
}

/* Destructor */
Lexer::~Lexer() {
	table.clear();
	lineScanner.clear();
}

/** Finds the next non-blank text in the input file. If the file is finished, it
 * returns the text "TEOF". */
string Lexer::nextText() {
	string text;

	do {
		text = "";

		// Iterate to next line or declare file ending
		if(lineScanner.length() == 0) {
			if(!fileScanner.eof()) {
				getline(fileScanner, lineScanner, '\n');
				lineNumber += 1;
			}
			else
				text = "TEOF";
		}
		// Obtain non empty string
		else {
			if(lineScanner.find(" ") != string::npos) {
				text = lineScanner.substr(0, lineScanner.find(" "));
				lineScanner = lineScanner.substr(lineScanner.find(" ") + 1,
												 lineScanner.length() - 1);
			}
			else {
				text = lineScanner.substr(0,lineScanner.length());
				lineScanner.clear();
			}
		}
	} while (text.length() == 0);

	return text;
}

/** Returns the next token without the given text, as the parser only processes
 * the codes to verify the grammar. */
Token* Lexer::nextToken() {
	string text = nextText();

	// Check if text is a valid keyword
	for(Token t : table) {
		string comparar = t.getText();
		if(comparar.compare(text) == 0)
			return new Token(t.getCode(), text);

	}

	// Check if text is a valid variable name
	if (validVariableName(text)) return new Token(VARIABLE, text);

	// Check if text is a valid constant
	if (validConstant(text, INT)) return new Token(CONSTANT, text);
	if (validConstant(text, FLOAT)) return new Token(CONSTANT, text);

	return new Token(INVALIDTOKEN, "");
}

/** Returns true if the parameter is a character. */
bool isLetter(char c) {
   return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

/** Returns true if the parameter is a number. */
bool isNumber(char c) {
	return '0' <= c && c <= '9';
}

/** Returns true if the parameter is a valid variable name. A valid variable
 * name does not start with a number and it is only composed by letters and
 * numbers. */
bool Lexer::validVariableName(string text)
{
	for(int i = 0; i < text.length(); i++) {
		char letter = text[i];
		if (i == 0 && isNumber(letter)) return false;
		if(!isLetter(letter) && !isNumber(letter)) return false;
	}
	return true;
}

/** Returns true if the string is a float number */
bool isFloat(string text) {
    bool foundPoint = false;
    for (char num : text) {
        if(!isdigit(num) && num != '.') {
            return false;
        }
        if (!foundPoint && num == '.') foundPoint = true;
        else if (foundPoint && num == '.') return false;
    }
    return true;
}

/** Returns true if the string is an integer number */
bool isInt(string text) {
	for (char num : text) {
		if (!isdigit(num)) return false;
	}
	return true;
}

/** Returns true if the string is a valid constant */
bool Lexer::validConstant(string text, int code){
	return code == INT ? isInt(text) : isFloat(text);
}

/** Given the numerical code of a token, return the text associated with the
 * token. Used to make the error reporting in the Parser more readable. */
string Lexer::getTokenText(int code) {
	for(auto t: table) {
		if(t.getCode() == code) return t.getText();
	}
	return "";
}

/** Gets the current line number that the lexer is parsing. */
int Lexer::getLineNumber() {
	return lineNumber;
}
