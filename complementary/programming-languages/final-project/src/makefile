compilador: saul.o parser.o saulrunner.o saultree.o
	g++ -g -o saul saul.o parser.o lexer.o token.o saulrunner.o function.o saultree.o

saul.o: saul.cpp parser.o saultree.o
	g++ -g -c saul.cpp

saulrunner.o: lexer.o function.o saulrunner.h saultree.o
	g++ -g -c saulrunner.cpp

function.o: lexer.o function.h saultree.o
	g++ -g -c function.cpp

saultree.o: saultree.h
	g++ -g -c saultree.cpp

parser.o: parser.cpp parser.h lexer.o
	g++ -g -c parser.cpp

lexer.o: lexer.cpp lexer.h token.o token.h
	g++ -g -c lexer.cpp

token.o: token.cpp token.h
	g++ -g -c token.cpp

clean:
	rm -f *.o
