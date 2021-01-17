/**
 * Class for storing a token. - Adapted to C++
 * It has two attributes: the numeric code and (possibly) the text
 *
 * @author Helmuth Trefftz
 * @author Juan Sebastián Cárdenas Rodríguez
 */
#include <string>
#include "token.h"

using namespace std;

/** The token is constructed based in a given code and the string that the token
 * represents. */
Token::Token(int code, string text) {
	this->code = code;
	this->text = text;
}

/* Destructor */
Token::~Token() {
	text.clear();
}

/** This method returns in a string all the information of the token. */
string Token::toString() {
	return "(" + to_string(code) + "," + text + ")";
}

/** Obtain text */
string Token::getText() {
	return text;
}

/** Obtain code */
int Token::getCode() {
	return code;
}
