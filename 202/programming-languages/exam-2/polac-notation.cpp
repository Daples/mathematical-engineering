#include <iostream>
#include <vector>
#include <string>
#include <array>
#include <sstream>

using namespace std;

/* Generalized class that handles each of the tokens. This class is requested
 * by the second question of the exam. */
class Token {
    private:
        string token;
        array<char, 4> ops = { '+', '-', '/', '*' };

    public:
        Token(string token) {
            this -> token = token;
        }
        bool isNum();
        bool isOp();
        double getResult(double num1, double num2);
        double getNum();
        string getToken();
};

// Abstract type to represent a vector of elements of type Token.
using Tokens = vector<Token>;

/* ================= Token Functions ================= */
/* This function returns if a given token is a number. */
bool Token::isNum() {
    bool foundPoint = false;
    for (char num : token) {
        if(!isdigit(num) && num != '.') {
            return false;
        }
        if (!foundPoint && num == '.') foundPoint = true;
        else if (foundPoint && num == '.') return false;
    }
    return true;
}

/* This function returns if a given token is a operator, such as multiplication
 * or division. */
bool Token::isOp() {
    for (char op : ops) {
        if (op == token[0])
            return true;
    }
    return false;
}

/* This functions gives the result of an operation, when the token is a
 * respective operator. */
double Token::getResult(double num1, double num2) {
    if (token[0] == '+')
        return num1 + num2;
    else if (token[0] == '*')
        return num1 * num2;
    else if (token[0] == '-')
        return num1 - num2;
    return num1 / num2;
}

/* This function transforms a token that is a number to a digit. */
double Token::getNum() {
    return stod(token);
}

/* This function gets the string of the token. */
string Token::getToken() {
    return token;
}

/* ================= Polac Expression Functions ================= */
/* This function reads all the tokens from a given line. */
Tokens getTokens(string expr) {
    string aux = "";
    bool foundSpace = false;
    bool first = true;
    for (int i = 0; i < expr.size(); i++) {
        if (foundSpace && expr[i] == ' ') continue;

        if (first && expr[i] == ' ') continue;
        else if (first) first = false;

        if (!foundSpace && expr[i] == ' ')
            foundSpace = true;
        if (foundSpace && expr[i] != ' ')
            foundSpace = false;
        aux += expr[i];
    }
    stringstream chain (aux);
    string token;
    Tokens tokens;
    while (getline(chain, token, ' '))
        tokens.push_back(token);
    return tokens;
}

/* This function shows if a given vector of tokens represents a valid expression
 * in polish notation. This function is requested for the third question of the
 * exam. */
bool isValidExpression(Tokens tokens) {
    if (tokens.size() < 3)
        return false;
    int i = tokens.size() - 1;
    if (!tokens[i].isNum())
        return false;
    i -= 1;

    // Iterate over the expression
    int unusedNumbers = 1;
    while (i >= 0) {
        if (tokens[i].isOp() && unusedNumbers == 1)
            return false;
        else if (tokens[i].isOp() && unusedNumbers != 1) {
            unusedNumbers -= 1;
            i -= 1;
        }
        else if (i >= 1 && tokens[i - 1].isOp() && tokens[i].isNum()) {
            i -= 2;
        }
        else if (i >= 1 && tokens[i - 1].isNum()) {
            unusedNumbers += 1;
            i -= 1;
        }
        else return false;
    }
    return unusedNumbers == 1;
}

/* This function calculates the result of a given vector of tokens that are
 * well-formed. In case that a division by 0 is found, the error is handled to
 * show "Math Overflow". This function is required for the fourth question of
 * the exam. */
pair<bool, double> getResultExpression(Tokens tokens) {
    int i = tokens.size() - 1;
    vector<double> stack;
    stack.push_back(tokens[i].getNum());
    i -= 1;
    bool success = true;

    // Iterate over the expression
    while (i >= 0) {
        if (tokens[i].isOp()) {
            if (tokens[i].getToken()[0] == '/' && stack.back() == 0) {
                success = false;
                break;
            }
            double ansNum = stack.back();
            stack.pop_back();
            stack[stack.size() - 1] = tokens[i].getResult(ansNum, stack.back());
            i -= 1;
        }
        else if (i >= 1 && tokens[i - 1].isOp() && tokens[i].isNum()) {
            if (tokens[i - 1].getToken()[0] == '/' && stack.back() == 0) {
                success = false;
                break;
            }
            stack[stack.size() - 1] = tokens[i - 1].getResult(tokens[i].getNum(), stack.back());
            i -= 2;
        }
        else if (i >= 1 && tokens[i - 1].isNum()) {
            stack.push_back(tokens[i].getNum());
            i -= 1;
        }
    }
    return pair<bool, double>(success, stack.back());
}

/* This function reads a number of expressions from the command line and stops
 * when the character "#" is found. This function is required by the first
 * question of the exam.  */
vector<Tokens> readExpressions() {
    string expr;
    vector<Tokens> expressions;
    cout << "Write an expression to be compiled an press enter: ";
    getline(cin, expr);
    while (expr != "#") {
        expressions.push_back(getTokens(expr));
        cout << "Write an expression to be compiled an press enter: ";
        getline(cin, expr);
    }
    return expressions;
}

/* Final program that allows to enter multiple expressions to be compiled and
 * found. This function is required by the last question of the exam. */
int main() {
    cout << "---- Polac Expression Compiler ----" << endl;
    cout << "The available operations are:\n\t*: multiplication.\n\t/: division.";
    cout << "\n\t+: sum.\n\t-: subtraction." << endl;
    cout << "To stop reading expressions input the character #\n" << endl;
    vector<Tokens> expressions = readExpressions();
    int i = 1;
    cout << endl << "---- Results of expressions ----" << endl;
    for (Tokens expr : expressions) {
        cout << i << ". ";
        if (!isValidExpression(expr)) {
            cout << "Syntax error." << endl;
            continue;
        }
        pair<bool, double> result = getResultExpression(expr);
        if (result.first)
            cout << "It is equals to " << result.second << endl;
        else
            cout << "A division by 0 was encountered, Math Overflow." << endl;
        i += 1;
    }
}
