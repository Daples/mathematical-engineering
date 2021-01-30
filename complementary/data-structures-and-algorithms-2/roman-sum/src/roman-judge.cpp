#include <array>
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <vector>

using namespace std;
using TupleRanges = array<array<int, 2>, 3>;
class Problem {
  int DISCARD_THIS = -1;
  int DISCARD_FORWARD = -2;
  public:
    string first, second, ans;
    array<int, 7> indexes = { -1, -1, -1, -1, -1, -1, -1 };
    vector<array<int, 2>> ranges;
    vector<int> start;
    vector<int> list;
    array<bool, 10> used = { false };
    int maxIndex = -1;
    Problem(string line) {
      int indexPlus = line.find('+');
      int indexEqual = line.find('=');
      first = line.substr(0, indexPlus);
      second = line.substr(indexPlus + 1, indexEqual - indexPlus - 1);
      ans = line.substr(indexEqual + 1);
      if (second.length() < first.length()) {
        string temp = first;
        first = second;
        second = temp;
      }
    };
    void solveRomanPart();
    void correctList();
    bool initializeLists();
    bool nextCombination();
    bool updateList(int i);
    bool backTrack();
    string backTrackAlgorithm();
    bool necessaryConditions();
    void solveArabicPart();
    bool testSolution();
    int transformNumber(string str);
};
int romanCharToInteger(char c) {
  switch (c) {
    case 'M':
      return 1000;
    case 'D':
      return 500;
    case 'C':
      return 100;
    case 'L':
      return 50;
    case 'X':
      return 10;
    case 'V':
      return 5;
    default:
      return 1;
  }
}
int romanCharToIndex(char c) {
  switch (c) {
    case 'M':
      return 0;
    case 'D':
      return 1;
    case 'C':
      return 2;
    case 'L':
      return 3;
    case 'X':
      return 4;
    case 'V':
      return 5;
    default:
      return 6;
  }
}
int romanToInteger(string roman) {
  int lastChar = romanCharToInteger(roman[0]);
  int num = lastChar;
  for(unsigned int i = 1; i < roman.size(); i++) {
    int actualChar = romanCharToInteger(roman[i]);
    if (lastChar < actualChar) num -= 2 * lastChar;
    num += actualChar;
    lastChar = actualChar;
  }

  return num;
}
void Problem :: solveRomanPart() {
  int firstNum = romanToInteger(first);
  int ansNum = romanToInteger(ans);
  string output = "Incorrect";
  if (firstNum < ansNum && firstNum + romanToInteger(second) == ansNum)
    output = "Correct";
  cout << output << " ";
}
pair<array<int, 2>, bool> intersectRanges(array<int,2> range1, array<int, 2> range2) {
  array<int, 2> range = { range1[0], range1[1] };
  if (range[1] < range2[0] || range2[1] < range[0])
    return pair<array<int, 2>, bool>(range, false);

  if (range[0] < range2[0])
    range[0] = range2[0];

  if (range2[1] < range[1])
    range[1] = range2[1];

  return pair<array<int, 2>, bool> (range, true);
}
bool fillNumbers(Problem *prob) {
  for (unsigned int j = 0; j < (prob -> ranges).size(); j++) {
    (prob -> list).push_back(-1);
    (prob -> start).push_back(-1);
    array<int, 2> range = (prob -> ranges)[j];
    if (range[0] == range[1]) {
      if (!(prob -> used)[range[1]]) {
        (prob -> list)[j] = range[1];
        (prob -> start)[j] = range[1];
        (prob -> used)[range[1]] = true;
      }
      else return false;
    }
  }
  for (unsigned int i = 0; i < (prob -> ranges).size(); i++) {
    array<int, 2> range = (prob -> ranges)[i];
    if (range[0] == range[1]) continue;
    for (int j = range[0]; j <= range[1]; j++) {
      if (!(prob -> used)[j]) {
        (prob -> list)[i] = j;
        (prob -> start)[i] = j;
        (prob -> used)[j] = true;
        break;
      }
    }
    if ((prob -> list)[i] == -1)
      return false;
  }
  return true;
}
bool fillRanges(string str, int i, Problem *prob, array<int, 2> range) {
  int index = str.length() + i;
  if (index < 0)
    return true;
  char letter = str[index];
  int indexLetter = romanCharToIndex(letter);
  if ((prob -> indexes)[indexLetter] == -1) {
    (prob -> indexes)[indexLetter] = (prob -> ranges).size();
    if (i == -1) {
      prob -> maxIndex = max(prob -> maxIndex, (prob -> indexes)[indexLetter]);
    }
    (prob -> ranges).push_back(range);
  }
  else {
    int indexMap = (prob -> indexes)[indexLetter];
    pair<array<int, 2>, bool> rangesSuccess = intersectRanges(range, (prob -> ranges)[indexMap]);
    if (!rangesSuccess.second) return false;
    (prob -> ranges)[indexMap] = rangesSuccess.first;
  }
  return true;
}
TupleRanges obtainRanges(Problem *prob, int i) {
  array<int, 3> lengths = { (int) (prob -> first).length(), (int) (prob -> second).length(),
                            (int) (prob -> ans).length() };
  TupleRanges ranges;
  for (int j = 0; j < 3; j++) {
    bool setMaxima = false;
    int index = lengths[j] + i;
    bool condition1 = lengths[2] > lengths[1];
    bool condition2 = lengths[0] < lengths[1];
    if (index == 0) {
      ranges[j][0] = 1;
      if (j == 2 && condition1) {
        ranges[j][1] = 1;
        setMaxima = true;
      }
      else if (j == 1 && condition1 && condition2) ranges[j][0] = 9;
    }
    else ranges[j][0] = 0;
    if (j == 2 && index == 1 && condition1 && condition2) {
      ranges[j][1] = 0;
      setMaxima = true;
    }
    if (!setMaxima) ranges[j][1] = 9;

  }
  return ranges;
}
bool Problem :: initializeLists() {
  int maxLength = max(ans.length(), second.length());
  bool feasible = true;
  for (int i = -1; i >= -maxLength; i--) {
    TupleRanges ranges = obtainRanges(this, i);
    feasible = feasible && fillRanges(first, i, this, ranges[0]);
    feasible = feasible && fillRanges(second, i, this, ranges[1]);
    feasible = feasible && fillRanges(ans, i, this, ranges[2]);
    if (!feasible) break;
  }
  if (feasible) feasible = feasible && fillNumbers(this);
  return feasible;
}
bool Problem :: updateList(int initialIndex) {
  for (int i = initialIndex; i >= 0; i--) {
    used[list[i]] = false;
    do {
      list[i] = (list[i] + 1) % (ranges[i][1] + 1);
      if (list[i] < ranges[i][0]) list[i] = ranges[i][0];
      if (list[i] == start[i]) break;
    } while (used[list[i]]);

    if (list[i] != start[i]) {
      used[list[i]] = true;
      return true;
    }

    if (i == 0) return false;
    list[i] = DISCARD_THIS;
  }
  return true;
}
void Problem :: correctList() {
  bool restartForward = false;
  for (unsigned int i = 0; i < list.size(); i++) {
    restartForward = restartForward || list[i] == DISCARD_FORWARD;
    if (!restartForward && list[i] != DISCARD_THIS) continue;
    for (int j = ranges[i][0]; j <= ranges[i][1]; j++) {
      if (!used[j]) {
        list[i] = j;
        start[i] = j;
        used[j] = true;
        break;
      } else list[i] = start[i];
    }
  }
}
bool Problem :: nextCombination() {
  bool nextList = updateList(list.size() - 1);
  correctList();
  return nextList;
}
int Problem :: transformNumber(string str) {
  int num = 0;
  int pow = 1;
  for (int i = str.length() - 1; i >= 0; i--) {
    num += pow * list[indexes[romanCharToIndex(str[i])]];
    pow *= 10;
  }
  return num;
}
bool Problem :: testSolution() {
  int secondNum = transformNumber(second);
  int ansNum = transformNumber(ans);
  return secondNum < ansNum && transformNumber(first) + secondNum == ansNum;
}
bool Problem :: necessaryConditions() {
  return second.length() <= ans.length() && ans.length() <= second.length() + 1;
}

bool Problem :: backTrack() {
  int indexFirst = indexes[romanCharToIndex(first[first.length() - 1])];
  int indexSecond = indexes[romanCharToIndex(second[second.length() - 1])];
  int indexAns = indexes[romanCharToIndex(ans[ans.length() - 1])];
  bool feasible = true;
  bool restartedAll = false;
  while ((list[indexFirst] + list[indexSecond]) % 10 != list[indexAns]) {
    if (!restartedAll) {
      restartedAll = true;
      for (unsigned int i = maxIndex + 1; i < list.size(); i++) {
        if (ranges[i][0] != ranges[i][1])
          used[list[i]] = false;
      }
    }
    feasible = updateList(maxIndex);
    if (!feasible) break;
    correctList();
    if ((list[indexFirst] + list[indexSecond]) % 10 == list[indexAns]) {
      list[maxIndex + 1] = DISCARD_FORWARD;
      correctList();
    }
  }
  return feasible;
}
string Problem :: backTrackAlgorithm() {
  string output = "impossible";
  if (!initializeLists()) return output;
  int solutions = 0;
  do {
    bool feasible = backTrack();
    if (!feasible) break;
    if (testSolution()) solutions += 1;
    if (solutions >= 2) break;

  } while (nextCombination());

  if (solutions == 1) output = "valid";
  else if (solutions >= 2) output = "ambiguous";

  return output;
}
void Problem :: solveArabicPart() {
  string output = "impossible";
  if (necessaryConditions()) output = backTrackAlgorithm();
  cout << output << endl;
}
vector<Problem> readInput() {
  string eq;
  cin >> eq;
  vector<Problem> problems;
  while (eq != "#") {
    problems.push_back(Problem (eq));

    cin >> eq;
  }
  return problems;
}
int main () {
  vector<Problem> problems = readInput();
  for (Problem prob : problems) {
    prob.solveRomanPart();
    prob.solveArabicPart();
  }
  return 0;
}
