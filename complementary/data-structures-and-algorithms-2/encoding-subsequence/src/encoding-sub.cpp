#include "iostream"
#include "string"
#include "vector"

using namespace std;

/* Main algorithm. Checks if an input is encoded by the string encoded. */
void isSubsqeuence(string input, string encoded) {
    int j = 0;
    for (int i = 0; i < encoded.size(); i++) {
        if (input[j] == encoded[i])
            j++;
        if (j == input.size()) {
            cout << "Yes" << endl;
            return;
        }
    }
    cout << "No" << endl;
}

/* It parses all the standard input, saves it in a vector and passes it to the
 * function that solves the respective problem. */
int main() {
    // Read problem
    string line;
    vector<string> problems;
    while (getline(cin, line)) {
        problems.push_back(line);
    }

    // Solve each of them
    for (string prob : problems) {
        int indexSpace = prob.find(' ');

        string input = prob.substr(0, indexSpace);
        string encoded = prob.substr(indexSpace + 1);
        isSubsqeuence(input, encoded);
    }
}
