/**
 * The Spanish Amateur Unpractical Language (SAUL). Based on the code given by
 * the teacher, subject Programming Languages.
 *
 * @author Juan Sebastián Cárdenas
 * @author Manuela Gallego Gómez Ossa
 */

#include <iostream>
#include <string>
#include "parser.h"
#include "saulrunner.h"

using namespace std;

/** Main for the SAUL executable. */
int main(int argc, char* argv[]) {
    if (argc == 1)
        cout << "SAUL necesita un archivo para procesar." << endl;
    if (argc > 2)
        cout << "SAUL solo procesa un archivo al tiempo." << endl;

    // Parse the file
    Parser* parser = new Parser(argv[1]);
    parser -> program();

    // Run file
    SaulRunner* sr = new SaulRunner(argv[1]);
    sr -> runProgram();

    return 0;
}
