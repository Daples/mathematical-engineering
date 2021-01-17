#ifndef saultree_h
#define saultree_h

#include "string"
#include "vector"

using namespace std;

/* ====== SaulTree ====== */
/** The saultree class represents a tree that performs mathematical operations
 * using the available operators. */
class SaulTree {
    private:
        // Attributes
        string op;
        SaulTree* treeLeft;
        SaulTree* treeRight;
        double value;

        // Functions
        void printTree(SaulTree* st);

    public:
        SaulTree(string op, double value);
        bool isNumber();
        void setTreeLeft(SaulTree* treeLeft);
        void setTreeRight(SaulTree* treeRight);
        SaulTree* getTreeLeft();
        SaulTree* getTreeRight();
        double calculate();
        double getValue();
        string getOp();
        void print();
};

/* ====== SaulCalculator ====== */
/** The saulcalculator class is a proxy to use the saultree class. It transforms
 * tokens to a tree that can be calculated using the prior class. This allows
 * for an easier and more readable interaction. */
class SaulCalculator {
    private:
        // Operation priority
        string opsOrder[4] = { "*", "/", "+", "-" };

    public:
        SaulCalculator();
        SaulTree* getTreeWithNoParen(vector<SaulTree*> trees, vector<string> ops);
        double calculateExpression(vector<string> fact);
};

#endif
