compilador: saul.o parser.o
	g++ -g -o saul saul.o parser.o lexer.o token.o

compiladorV01.o: saul.cpp parser.o
	g++ -g -c saul.cpp

parser.o: parser.cpp parser.h lexer.o
	g++ -g -c parser.cpp

lexer.o: lexer.cpp lexer.h token.o token.h
	g++ -g -c lexer.cpp

token.o: token.cpp token.h
	g++ -g -c token.cpp

clean:
	rm -f *.o
