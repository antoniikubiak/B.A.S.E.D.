# B.A.S.E.D. - Broad Arithmetic Symbolic Expression Derivator
B.A.S.E.D. is aimed to be a symbolic expression compiler designed to transform complex mathematical notation into optimized C code.
Authors:
- Antoni Kubiak antonikubiak@student.agh.edu.pl,
- Szymon Król szymonkrol@student.agh.edu.pl.

Basics:
- Mathematical expressions compiler
- Result: C code
- Implementation language: Python 3
- Parser generator: Lark

## Core Objectives

The primary goal of B.A.S.E.D. is to transform abstract mathematical definitions into executable C code. The project focuses on the following aspects:

- Symbolic manipulation: Handling derivatives and algebraic manipulations at the symbolic level.

- Algebraic optimization: Reducing complexity through constant folding, algebraic simplification (e.g., x+x->2x), and Common Subexpression Elimination (CSE).

- Compilation: generating C functions that can be integrated into larger systems.

## Key Features

1. Expression
Support for a rich mathematical grammar including:
- Standard arithmetic (+,−,∗,/) and exponentiation.
- Elementary functions: sin, cos, log, exp.
- Finite sum and product notation: Converting `sum(n from start to end: expr)` into either loops or algebraic constants.
- Ability to define piecewise functions: `if-else` syntax may enable the user to define expressions differently based on various inputs.

2. Symbolic derivation engine
Users can define functions and request derivatives with respect to specific variables. The compiler applies the chain rule and power rule recursively to generate the derivative expression before passing them on.

3. Optimization
That part includes:
- Common subexpression elimination: identifying repeated terms (like x2 or sin(y)) and assigning them to temporary variables (t0​,t1​) to prevent redundant calculations. That is done by converting expression parse tree into directed acyclic graph by merging nodes containing the same expressions.
- Constant folding: pre-calculating values that do not depend on input variables (e.g., the sum of 1…10 becomes 55).
- Identity reduction: eg. simplifying 0⋅x to 0 and 1⋅x to x

## Simple examples
For input:
```
f(x) := x+2;
g(x, y) := x^2+sin(y) + 1;
> f(x) + 2*g(x, x) + sin(x) as foo(int x) -> double;
```
The resulting C function could be:
``` C
double foo(x) {
	double t0 = sin(x);
	return 2*x*x + x + 4 + 3*t0;
}
```
For input:
```
> sum(n from 1 to 10: n*x^2) as foo() -> double
```
The resulting C function could be:
``` C
double foo(x) {
	return 55*x*x;
}
```

## Token Table for B.A.S.E. grammar
| Token Name   | Pattern / Value                            | Description                                                                                       |
|:-------------|:-------------------------------------------|:--------------------------------------------------------------------------------------------------|
| BOOL_CONST   | `true` \| `false`                          | Boolean literals.                                                                                 |
| TYPE         | `double` \| `float` \| `int`               | C-style data types used to specify the output format and parameter types of the generated C code. |
| REL_OP       | `==` \| `!=` \| `>` \| `<` \| `>=` \| `<=` | Relational comparison operators.                                                                  |
| IDENTIFIER   | `[a-zA-Z_][a-zA-Z0-9_]*`                   | User-defined names for mathematical functions, variables, and the final exported C function.      |
| NUMBER       | `\d+(.\d+)?([eE][+-]?\d+)?`                | Numeric literals.                                                                                 |
| INT          | `[1-9][0-9]*`                              | Positive integers used specifically for the bounds of `sum`/`prod` or the order of a `diff`.      |
| ASSIGN       | `:=`                                       | The assignment operator.                                                                          |
| IF           | `if`                                       | Initiates a piecewise expression block.                                                           |
| ELIF         | `elif`                                     | Allows for alternative conditional branches within a single piecewise expression.                 |
| ELSE         | `else`                                     | Defines the default expression to be evalated.                                                    |
| THEN         | `then`                                     | Separates the condition from the expression to be evaluated if the condition is met.              |
| AND          | `and`                                      | Logical conjunction.                                                                              |
| OR           | `or`                                       | Logical disjunction.                                                                              |
| PLUS         | `+`                                        | Arithmetic addition operator.                                                                     |
| MINUS        | `-`                                        | Arithmetic subtraction or unary negation operator.                                                |
| STAR         | `*`                                        | Arithmetic multiplication operator.                                                               |
| SLASH        | `/`                                        | Arithmetic division operator.                                                                     |
| HAT          | `^`                                        | Exponentiation operator.                                                                          |
| SUM          | `sum`                                      | Keyword for 'Sigma' notation, used to define iterative addition over a specified range.           |
| PROD         | `prod`                                     | Keyword for 'Pi' notation, used to define iterative multiplication over a specified range.        |
| FROM         | `from`                                     | Keyword indicitaing the beggining of the range for shrothand 'Pi' or 'Sigma' notation.            |
| TO           | `to`                                       | Keyword indicitaing the end of the range for shrothand 'Pi' or 'Sigma' notation.                  |
| DIFF         | `diff`                                     | Derivative expression keyword.                                                                    |
| TARGET_START | `>`                                        | Syntactic marker indicating the start of a C-function signature generation.                       |
| AS           | `as`                                       | Keyword indictaing the name of C-function to be generated.                                        |
| ARROW        | `->`                                       | Syntax indicating the transition to the return type of the generated C function.                  |
| PUNCTUATION  | `(`, `)`, `,`, `:`, `;`                    | Syntactic delimiters.                                                                             |
| WS           | `[ \t\f\r\n]+`                             | Ignored characters.                                                                               |

## Lark grammar for B.A.S.E.D.
```lark
start: definition* target+

definition: IDENTIFIER "(" param_list? ")" ":=" expression ";"

param_list: IDENTIFIER ("," IDENTIFIER)*

target: ">" expression "as" IDENTIFIER "(" param_w_type_list? ")" "->" TYPE ";"

param_w_type_list: TYPE IDENTIFIER ("," TYPE IDENTIFIER)*

?expression: "if" condition "then" expression ("elif" condition "then" expression)* "else" expression
           | expr

?condition: log_or

?log_or: log_and ("or" log_and)*
?log_and: comparison ("and" comparison)*

?comparison: BOOL_CONST
           | expr REL_OP expr
           | "(" condition ")"

?expr: term (("+" | "-") term)*
?term: factor (("*" | "/") factor)*
?factor: "-" factor
       | power
?power: atom ("^" power)?

?atom: NUMBER
     | IDENTIFIER
     | function_call
     | shorthand
     | derivative
     | "(" expression ")"

function_call: IDENTIFIER "(" arg_list? ")"
arg_list: expr ("," expr)*

shorthand: ("sum" | "prod") "(" IDENTIFIER "from" INT "to" INT ":" expression ")"
derivative: "diff" "(" IDENTIFIER "," INT "," expression ")"

BOOL_CONST.2: "true" | "false"

TYPE.2: "double" | "float" | "int"
REL_OP: "==" | "!=" | ">" | "<" | ">=" | "<="

%import common.CNAME -> IDENTIFIER
%import common.NUMBER
%import common.INT
%import common.WS
%ignore WS
```
