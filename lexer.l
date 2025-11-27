%option noyywrap
%option nounput
%option noinput
%{
#include "parser.h"
#include <string.h>
#include <stdlib.h>
%}

DIGIT [0-9]
LETTER [A-Za-z]
ID {LETTER}({LETTER}|{DIGIT}|_)*
NUMBER {DIGIT}+
TIME {DIGIT}{DIGIT}":"{DIGIT}{DIGIT}":"{DIGIT}{DIGIT}
WS [ \t\r]+
STRING \"([^\"\\]|\\.)*\"

%%
[ \t]+   { /* skip completamente */ }
"+"     { printf("[LEXER] OPERATOR: '+'\n"); return '+'; }
"-"     { printf("[LEXER] OPERATOR: '-'\n"); return '-'; }
"*"     { printf("[LEXER] OPERATOR: '*'\n"); return '*'; }
"/"     { printf("[LEXER] OPERATOR: '/'\n"); return '/'; }

{DIGIT}+ {
    printf("[LEXER] NUMBER: '%s'\n", yytext);
    yylval.num = atof(yytext);
    return NUMBER;
}

"POWERON" { return POWERON; }
"POWEROFF" { return POWEROFF; }
"SHOWTIME" { return SHOWTIME; }
"SETTIME" { return SETTIME; }
"SETALARM" { return SETALARM; }
"SETTIMER" { return SETTIMER; }
"NOTIFY" { return NOTIFY; }
"HEARTBEAT" { return HEARTBEAT; }
"STEP" { return STEP; }
"MUSICPLAY" { return MUSICPLAY; }
"MUSICSTOP" { return MUSICSTOP; }
"BLUETOOTH" { return BLUETOOTH; }
"HALT" { return HALT; }
"WHEN" { return WHEN; }
"THEN" { return THEN; }
"ELSE" { return ELSE; }
"ENDWHEN" { return ENDWHEN; }
"LOOP" { return LOOP; }
"DO" { return DO; }
"ENDLOOP" { return ENDLOOP; }
"CALL" { return CALL; }
"RETURN" { return RETURN; }
"ON" { return ON; }
"OFF" { return OFF; }
"SHOW" { return SHOW; }

{TIME} {
    yylval.str = strdup(yytext);
    return TIME_TOK;
}

{STRING} {
    yylval.str = strdup(yytext);
    return STRING;
}

{ID} {
    yylval.str = strdup(yytext);
    return IDENT;
}

[;#].* { /* skip comment */ }
{WS} { /* skip */ }
\n { return '\n'; }

"=="    { printf("[LEXER] Token EQ: ==\n"); return EQ; }
"!="    { printf("[LEXER] Token NEQ: !=\n"); return NEQ; }
"<="    { printf("[LEXER] Token LE: <=\n"); return LE; }
">="    { printf("[LEXER] Token GE: >=\n"); return GE; }
"<"     { printf("[LEXER] Token LT: <\n"); return LT; }
">"     { printf("[LEXER] Token GT: >\n"); return GT; }

"="     { return '='; }
":"     { return ':'; }
","     { return ','; }
"("     { return '('; }
")"     { return ')'; }

%%