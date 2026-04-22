# Token Table for B.A.S.E. grammar
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
