/**
 * The Spanish Amateur Unpractical Language (SAUL). Based on the code given by
 * the teacher, subject Programming Languages.
 *
 * @author Juan Sebastián Cárdenas
 */

#include <iostream>
#include <string>
#include "parser.h"

using namespace std;

/** Main for the SAUL executable. */
int main(int argc, char* argv[]) {
    if (argc == 1)
        cout << "SAUL necesita un archivo para procesar." << endl;

    // Parse each file
    for (int i = 1; i < argc; i++) {
        if (argc > 2) {
            cout << "Procesando archivo " << argv[i] << "..." << endl;
        }

        Parser* parser = new Parser(argv[i]);
        parser -> program();

        if (argc > 2) {
            cout << endl;
        }
    }

    return 0;
}
