#ifndef token_h
#define token_h

#include <string>

using namespace std;

/* ====== Token ====== */
/** The token class saves individually each of the elements for the SAUL
 * programming language. */
class Token {
    private:
        int code;
        string text;

    public:
        Token(int code, string text);
        virtual ~Token();
        string toString();
        string getText();
        int getCode();
};

#endif
