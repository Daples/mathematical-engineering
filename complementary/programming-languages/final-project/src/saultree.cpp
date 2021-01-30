#include "saultree.h"

#include "iostream"

using namespace std;

/* ====== SaulTree ====== */
/** Constructor for saul tree class. The tree recieves both a value and a
 * operator to simplify code. In case the tree represents a number only the
 * value is needed. On the other hand, both branches must be set. */
SaulTree::SaulTree(string op, double value) {
    this -> op = op;
    this -> value = value;
}

/* Getters */
SaulTree* SaulTree::getTreeLeft() {
    return treeLeft;
}

SaulTree* SaulTree::getTreeRight() {
    return treeRight;
}

double SaulTree::getValue() {
    return this -> value;
}

string SaulTree::getOp() {
    return this -> op;
}

/* Setters */
void SaulTree::setTreeLeft(SaulTree* treeLeft) {
    this -> treeLeft = treeLeft;
}

void SaulTree::setTreeRight(SaulTree *treeRight) {
    this -> treeRight = treeRight;
}

bool SaulTree::isNumber() {
    return !treeLeft;
}

/** This function calculates the result of all the mathematical expression
 * represented by the tree. */
double SaulTree::calculate() {
    if (this -> isNumber())
        return this -> getValue();

    if (this -> getOp() == "+") {
        return treeLeft -> calculate() + treeRight -> calculate();
    }
    else if (this -> getOp() == "-") {
        return treeLeft -> calculate() - treeRight -> calculate();
    }
    else if (this -> getOp() == "*") {
        return treeLeft -> calculate() * treeRight -> calculate();
    }
    else if (this -> getOp() == "/") {
        double calcRight = treeRight -> calculate();
        if (calcRight == 0) {
            cout << "División por cero, SAUL está triste." << endl;
            exit(3);
        }
        return treeLeft -> calculate() / calcRight;
    }
    return 0;
}

/* ====== SaulCalculator ====== */
/** Constructor for saul calculator class. */
SaulCalculator::SaulCalculator() {}

/** This function calculates a whole exprression, given as a vector of string
 * tokens that represent a mathematical expression.*/
double SaulCalculator::calculateExpression(vector<string> fact) {
    vector<vector<SaulTree*>> trees;
    vector<vector<string>> operations;

    // Base trees
    vector<SaulTree*> base;
    trees.push_back(base);
    vector<string> opBase;
    operations.push_back(opBase);

    for (int i = 0; i < fact.size(); i++) {
        // Indent in depth
        if (fact[i] == "(") {
            vector<SaulTree*> parenBase;
            vector<string> opsBase;
            trees.push_back(parenBase);
            operations.push_back(opsBase);
        }

        // Operation
        else if (fact[i] == "+" || fact[i] == "-" || fact[i] == "/" ||
                 fact[i] == "*"){
            operations[operations.size() - 1].push_back(fact[i]);
        }

        // Close depth
        else if (fact[i] == ")") {
            vector<SaulTree*> parenBase = trees.back();
            trees.pop_back();
            vector<string> opsBase = operations.back();
            operations.pop_back();

            SaulTree* st = getTreeWithNoParen(parenBase, opsBase);
            trees[trees.size() - 1].push_back(st);
        }

        // Add number
        else {
            trees[trees.size() - 1].push_back(new SaulTree("", stod(fact[i])));
        }
    }

    // Calculate expression
    base = trees.back();
    opBase = operations.back();
    SaulTree* finalExpression = getTreeWithNoParen(base, opBase);
    return finalExpression -> calculate();
}

/** This function calculates a mathematical expression that does not have any
 * parenthesis. This is used to get rid of parenthesis in the prior function
 * and to calculate the final expression. */
SaulTree* SaulCalculator::getTreeWithNoParen(vector<SaulTree*> elements,
                                             vector<string> ops) {
    for (string op : opsOrder) {
        vector<SaulTree*>::iterator itEl = elements.begin();
        for (vector<string>::iterator itOp = ops.begin(); itOp != ops.end(); ++itOp) {
            if (op == *itOp) {
                SaulTree* tree = new SaulTree(op, 0);
                tree -> setTreeLeft(*itEl);
                elements.erase(itEl);

                tree -> setTreeRight(*itEl);
                *itEl = tree;
                ops.erase(itOp);
                --itOp;
                continue;
            }
            ++itEl;
        }
    }
    return elements[0];
}

/** This function prints the tree using a recursive function. */
void SaulTree::print() {
    this -> printTree(this);
}

/** This function is an auxiliar function for printing a tree. */
void SaulTree::printTree(SaulTree* st) {
    if (st -> isNumber())
        cout << "Value: " << st -> getValue() << endl;
    else {
        cout << "Op: " << st -> getOp() << endl;
        printTree(st -> getTreeLeft());
        printTree(st -> getTreeRight());
    }
}
