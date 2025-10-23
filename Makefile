all: smartwatch

smartwatch: parser.c lexer.c
	gcc -o smartwatch parser.c lexer.c -lfl

parser.c parser.h: parser.y
	bison -d -o parser.c parser.y

lexer.c: lexer.l parser.h
	flex -o lexer.c lexer.l

clean:
	rm -f smartwatch parser.c parser.h lexer.c
