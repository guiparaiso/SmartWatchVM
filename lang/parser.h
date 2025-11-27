/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_H_INCLUDED
# define YY_YY_PARSER_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    EQ = 258,                      /* EQ  */
    NEQ = 259,                     /* NEQ  */
    LT = 260,                      /* LT  */
    LE = 261,                      /* LE  */
    GT = 262,                      /* GT  */
    GE = 263,                      /* GE  */
    IDENT = 264,                   /* IDENT  */
    STRING = 265,                  /* STRING  */
    TIME_TOK = 266,                /* TIME_TOK  */
    NUMBER = 267,                  /* NUMBER  */
    POWERON = 268,                 /* POWERON  */
    POWEROFF = 269,                /* POWEROFF  */
    SHOWTIME = 270,                /* SHOWTIME  */
    SETTIME = 271,                 /* SETTIME  */
    SETALARM = 272,                /* SETALARM  */
    SETTIMER = 273,                /* SETTIMER  */
    NOTIFY = 274,                  /* NOTIFY  */
    SHOW = 275,                    /* SHOW  */
    HEARTBEAT = 276,               /* HEARTBEAT  */
    STEP = 277,                    /* STEP  */
    MUSICPLAY = 278,               /* MUSICPLAY  */
    MUSICSTOP = 279,               /* MUSICSTOP  */
    BLUETOOTH = 280,               /* BLUETOOTH  */
    HALT = 281,                    /* HALT  */
    WHEN = 282,                    /* WHEN  */
    THEN = 283,                    /* THEN  */
    ELSE = 284,                    /* ELSE  */
    ENDWHEN = 285,                 /* ENDWHEN  */
    LOOP = 286,                    /* LOOP  */
    DO = 287,                      /* DO  */
    ENDLOOP = 288,                 /* ENDLOOP  */
    CALL = 289,                    /* CALL  */
    RETURN = 290,                  /* RETURN  */
    ON = 291,                      /* ON  */
    OFF = 292,                     /* OFF  */
    UMINUS = 293,                  /* UMINUS  */
    UPLUS = 294,                   /* UPLUS  */
    UNOT = 295                     /* UNOT  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 124 "parser.y"

  double num;
  char *str;

#line 109 "parser.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_PARSER_H_INCLUDED  */
