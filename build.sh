#!/bin/bash
echo "Building SmartWatch Language Compiler..."
cd lang/
bison -d parser.y
flex lexer.l
cd ..
gcc -o smartwatch lang/parser.c lang/lexer.c -lfl
echo "Build complete! Run with: ./smartwatch < program.sw"