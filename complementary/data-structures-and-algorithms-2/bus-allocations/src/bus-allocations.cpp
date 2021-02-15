#include "iostream"
#include "sstream"
#include "string"
#include "vector"

using namespace std;
typedef vector<int> vecInts;

/* ======== Bus problem abstract class ======== */
class BusProblem {
    private:
        vector<int> morningRoutes;
        vector<int> afternoonRoutes;
        int distanceToExtraPay;
        int rateOfExtraPay;

    public:
        BusProblem(int distanceToExtraPay, int rateOfExtraPay);
        void addMorningRoute(int route);
        void addAfternoonRoute(int route);
        void solveProblem();
};

/** Constructor for the bus problem. */
BusProblem::BusProblem(int distanceToExtraPay, int rateOfExtraPay) {
    this -> distanceToExtraPay = distanceToExtraPay;
    this -> rateOfExtraPay = rateOfExtraPay;
}

/* ======== Bus problems methods ======== */
/** This method adds a value to a vector of integers sorted. */
void addSortedVector(vecInts& vec, int value) {
    vecInts::iterator it = lower_bound(vec.begin(), vec.end(), value);
    vec.insert(it, value);
}

/** This method adds the distance of a morning routine to the correspondent
 * vector sorted. */
void BusProblem::addMorningRoute(int route) {
    addSortedVector(this -> morningRoutes, route);
}

/** This method adds the distance of a afternoon routine to the correspondent
 * vector sorted. */
void BusProblem::addAfternoonRoute(int route) {
    addSortedVector(this -> afternoonRoutes, route);
}

/** This algorithm finds the minimum cost of overpaying and outputs it through
 * cout. This solution takes advantage of the sorted arrays. */
void BusProblem::solveProblem() {
    int cost = 0;
    for (int i = 0; i < morningRoutes.size(); i++ ) {
        int auxIndex = afternoonRoutes.size() - i - 1;
        int distance = morningRoutes[i] + afternoonRoutes[auxIndex];

        int diff = distance - distanceToExtraPay;
        cost += diff > 0 ? diff : 0;
    }
    cout << cost * (this -> rateOfExtraPay) << endl;
}

/* ======== Main ======== */
/** This method reads each problem from the cin iostream and returns a vector of
 * objects of type BusProblem corresponding to each of the problems to solve. */
vector<BusProblem> readProblems() {
    vector<BusProblem> problems;
    string line;

    getline(cin, line);
    while (line != "0 0 0") {
        // Read main numbers
        stringstream chain (line);
        string token;

        getline(chain, token, ' ');
        int n = stoi(token);

        getline(chain, token, ' ');
        int d = stoi(token);

        getline(chain, token, ' ');
        int r = stoi(token);

        // Problem creation
        BusProblem problem (d, r);

        // Morning routine saving
        getline(cin, line);
        for (int i = 0; i < n; i++) {
            int indexSpace = line.find(" ");

            string token = line.substr(0, indexSpace);
            problem.addMorningRoute(stoi(token));
            line = line.substr(indexSpace + 1);
        }

        // Afternoon routine saving
        getline(cin, line);
        for (int i = 0; i < n; i++) {
            int indexSpace = line.find(" ");

            string token = line.substr(0, indexSpace);
            problem.addAfternoonRoute(stoi(token));
            line = line.substr(indexSpace + 1);
        }

        // Add problem to list
        problems.push_back(problem);
        getline(cin, line);
    }

    return problems;
}

/** This method solves each of the problems and outputs the desired solution. */
int main() {
    vector<BusProblem> busProblems = readProblems();
    for (BusProblem problem : busProblems) {
        problem.solveProblem();
    }
    return 0;
}
