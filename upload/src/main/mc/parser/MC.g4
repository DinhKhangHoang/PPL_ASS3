//1711679

grammar MC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text[1:]);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text[1:]);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text);
    else:
        return super().emit();
}

options{
	language=Python3;
}

program  : (decl)+ EOF;

decl : vardecl | funcdecl;

vardecl: primitivetype listvar SEMI ;

primitivetype: BOOLEAN|INTTYPE|FLOATTYPE|STRING;

listvar: var (CM var)*;

var: ID (LSB INTLIT RSB)?;

funcdecl: functype funcname LB listparam RB blockstmt;

functype : primitivetype
        | VOIDTYPE
        | arraypointertype;

funcname: ID;

listparam: (paradecl (CM paradecl)*)?;

paradecl: primitivetype ID (LSB RSB)?;

arraypointertype: primitivetype LSB RSB;

//stmt chua xong
stmt: ifstmt
        | whilestmt
        | forstmt
        | breakstmt
        | continuestmt
        | returnstmt
        | exprstmt 
        | blockstmt;

exprstmt: expr SEMI;

breakstmt: BREAK SEMI;

continuestmt: CONTINUE SEMI;

blockstmt: LP (vardecl | stmt)* RP;

ifstmt : IF LB expr RB stmt (ELSE stmt)?;

whilestmt: DO stmt+ WHILE expr SEMI;

forstmt: FOR LB expr SEMI expr SEMI expr RB stmt;

returnstmt: RETURN expr? SEMI;

//expression:

expr :  expr1 (EQ | NEQ) expr1
        | <assoc=left> expr AND expr
        | <assoc=left> expr OR expr
        | <assoc=right> expr ASSIGN expr
        | expr1;

expr1:  expr2 (LT | LE | GT | GE) expr2
        | expr2;

expr2:  operand LSB expr RSB
        | <assoc=right> (SUB | NOT) expr2
        | <assoc=left> expr2 (DIV | MUL | MOD) expr2
        | <assoc=left> expr2 (ADD | SUB) expr2
        | operand;

operand: LB expr RB | INTLIT | BOOLLIT | FLOATLIT | STRINGLIT | funcall | ID;

funcall: ID LB listarg RB;

listarg: (expr (CM expr)*)? ;
//keywords
INTTYPE: 'int' ;

VOIDTYPE: 'void' ;

BOOLEAN : 'boolean';

BREAK : 'break';

CONTINUE : 'continue';

ELSE : 'else';

FOR : 'for';

FLOATTYPE:'float';

IF:'if';

RETURN:'return';

DO:'do';

WHILE:'while';

STRING:'string';

//operators:
ADD: '+';

MUL: '*';

SUB: '-';

DIV: '/';

NOT: '!';

MOD: '%';

OR: '||';

AND: '&&';

NEQ: '!=';

EQ: '==';

LT: '<';

GT: '>';

LE: '<=';

GE: '>=';

ASSIGN: '=';
//Literals:
fragment Point: '.';
fragment Number: [0-9]+;
fragment Fraction:[0-9]+;
fragment Exponent:('e'|'E') ('-')? Number;
FLOATLIT: Number Point Fraction Exponent?
        | Point Fraction Exponent?
        | Number Point Exponent?
        | Number Exponent;

BOOLLIT: 'true' | 'false';

INTLIT: [0-9]+;

STRINGLIT: '"' (~ [\\"\n\r] | ESCAPESEQUENCE)* '"'{
        self.text= self.text[1:-1]
};
fragment ESCAPESEQUENCE: '\\' [btnfr"\\];
//identifier
ID: [_a-zA-Z][_a-zA-Z0-9]* ;

//seperators:
LB: '(' ;

RB: ')' ;

LP: '{';

RP: '}';

SEMI: ';' ;

LSB: '[';

RSB: ']';

CM: ',';

WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs, newlines, formfeed, cariage return
// comment:
COMMENT : (('//' ~[\n\r]*)|('/*' .*? '*/')) -> skip ;
//errors
UNCLOSE_STRING: '"' (~ ["\\\n\r] | ESCAPESEQUENCE)*;
ILLEGAL_ESCAPE: '"' (~ ["\\\n\r] | ESCAPESEQUENCE)* '\\' ~[btnfr"\\];
ERROR_CHAR: .;