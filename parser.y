/* parser.y - Análise Sintatica Smartwatch */

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex(void);
extern int yylineno;
extern char *yytext;
void yyerror(const char *s);

int sintatic_errors = 0;

/* Tabela de variáveis */
typedef struct { char *name; int def; int use; } Var;
Var *vars = NULL;
int nvars = 0;

/* Tabela de labels */
typedef struct { char *name; int def; int call; } Lab;
Lab *labels = NULL;
int nlabels = 0;

void def_var(char *n) {
  for (int i = 0; i < nvars; i++) 
    if (strcmp(vars[i].name, n) == 0) { vars[i].def = 1; return; }
  vars = realloc(vars, sizeof(Var) * (nvars + 1));
  vars[nvars++] = (Var){strdup(n), 1, 0};
}

void use_var(char *n) {
  for (int i = 0; i < nvars; i++) 
    if (strcmp(vars[i].name, n) == 0) { vars[i].use = 1; return; }
  vars = realloc(vars, sizeof(Var) * (nvars + 1));
  vars[nvars++] = (Var){strdup(n), 0, 1};
}

void def_lab(char *n) {
  for (int i = 0; i < nlabels; i++) 
    if (strcmp(labels[i].name, n) == 0) { 
      if (labels[i].def) { fprintf(stderr, "Erro: Label '%s' duplicado\n", n); sintatic_errors++; }
      labels[i].def = 1; return; 
    }
  labels = realloc(labels, sizeof(Lab) * (nlabels + 1));
  labels[nlabels++] = (Lab){strdup(n), 1, 0};
}

void call_lab(char *n) {
  for (int i = 0; i < nlabels; i++) 
    if (strcmp(labels[i].name, n) == 0) { labels[i].call = 1; return; }
  labels = realloc(labels, sizeof(Lab) * (nlabels + 1));
  labels[nlabels++] = (Lab){strdup(n), 0, 1};
}

void check_sintatics() {
  printf("\n=== ANÁLISE SINTÁTICA ===\n");

  for (int i = 0; i < nvars; i++)
    if (!vars[i].def && vars[i].use) {
      fprintf(stderr, "Erro: Variável '%s' usada sem definição\n", vars[i].name);
      sintatic_errors++;
    }
  
  for (int i = 0; i < nlabels; i++)
    if (!labels[i].def && labels[i].call) {
      fprintf(stderr, "Erro: Label '%s' chamado sem definição\n", labels[i].name);
      sintatic_errors++;
    }
  
  printf("\n--- VARIÁVEIS ENCONTRADAS (%d) ---\n", nvars);
  for (int i = 0; i < nvars; i++) {
    printf("  [%2d] %-15s : %s, %s\n", 
           i + 1,
           vars[i].name,
           vars[i].def ? "✓ definida  " : "✗ indefinida",
           vars[i].use ? "usada" : "não usada");
  }
  
  printf("\n--- LABELS ENCONTRADOS (%d) ---\n", nlabels);
  for (int i = 0; i < nlabels; i++) {
    printf("  [%2d] %-15s : %s, %s\n",
           i + 1,
           labels[i].name,
           labels[i].def ? "✓ definido " : "✗ indefinido",
           labels[i].call ? "chamado" : "não chamado");
  }
  
  printf("\n=========================\n");
  printf("Erros sintáticos: %d\n", sintatic_errors);
}

%}

%union {
  double num;
  char *str;
}

%token <str> IDENT STRING TIME_TOK
%token <num> NUMBER
%token POWERON POWEROFF SHOWTIME SETTIME SETALARM SETTIMER NOTIFY SHOW
%token HEARTBEAT STEP MUSICPLAY MUSICSTOP BLUETOOTH HALT
%token WHEN THEN ELSE ENDWHEN LOOP DO ENDLOOP CALL RETURN
%token ON OFF EQ NEQ LE GE LT GT

%left '+' '-'
%left '*' '/'

%%

program: /* vazio */ 
  | program statement
  | program '\n'
  ;
statement:
    IDENT ':' { def_lab($1); }
  | instr
  | IDENT '=' expr { def_var($1); }
  | WHEN expr comparator expr THEN stmt_list opt_else ENDWHEN
  | LOOP expr comparator expr DO stmt_list ENDLOOP
  | CALL IDENT { call_lab($2); }
  | RETURN | HALT
  ;

instr:
    POWERON | POWEROFF | SHOWTIME | HEARTBEAT | STEP | MUSICSTOP
  | SETTIME TIME_TOK | SETALARM TIME_TOK | SETTIMER NUMBER
  | NOTIFY STRING | SHOW expr | MUSICPLAY IDENT | BLUETOOTH ON | BLUETOOTH OFF
  ;

stmt_list: /* vazio */ 
    | stmt_list statement ;
    | stmt_list '\n' ;

opt_else: /* vazio */ 
    | ELSE stmt_list ;
    | stmt_list '\n' ;

comparator: EQ | NEQ | LT | LE | GT | GE ;

expr:
    term
  | expr '+' term
  | expr '-' term
  ;

term:
    factor
  | term '*' factor
  | term '/' factor
  ;

factor:
    NUMBER
  | STRING
  | IDENT { use_var($1); }
  | '(' expr ')'
  ;

%%

void yyerror(const char *s) {
  fprintf(stderr, "Erro: %s (linha %d)\n", s, yylineno);
}

int main() {
  printf("Parser Smartwatch - Análise Sintatica\n");
  printf("======================================\n\n");
  
//   #ifdef YYDEBUG
//   yydebug = 1;
//   #endif
  
  if (yyparse() == 0) {
    printf("✓ Parsing OK\n");
    check_sintatics();
    return sintatic_errors > 0 ? 1 : 0;
  }
  fprintf(stderr, "✗ Parsing falhou\n");
  return 1;
}