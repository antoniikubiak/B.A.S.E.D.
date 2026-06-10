# B.A.S.E.D. - Broad Arithmetic Symbolic Expression Derivator

B.A.S.E.D. is aimed to be a symbolic expression compiler designed to transform complex mathematical notation into
optimized C code.
Authors:

- Antoni Kubiak: antonikubiak@student.agh.edu.pl,
- Szymon Król: szymonkrol@student.agh.edu.pl.

---

Basics:

- Mathematical expressions compiler
- Result: C code
- Implementation language: Python 3
- Parser generator: Lark

---

## Core Objectives

The primary goal of B.A.S.E.D. is to transform abstract mathematical definitions into executable C code.
By resolving algebraic complexities, executing identity reductions, and applying optimizations at compile time,
the program minimizes runtime calculation overhead. 

The program is a **compiler**. It acts statically: parsing mathematical statements, constructing Abstract Syntax Trees (ASTs)
and Directed Acyclic Graphs (DAGs), performing symbolic calculus transformations, and writing out a standalone `.c` file.

The project focuses on the following aspects:

- Symbolic manipulation: Handling derivatives and algebraic manipulations at the symbolic level.

- Algebraic optimization: Reducing complexity through constant folding, algebraic simplification (e.g., x+x->2x), and
  Common Subexpression Elimination (CSE).

- Compilation: generating C functions that can be integrated into larger systems.

## Key Features

1. Expression
   Support for a rich mathematical grammar including:

- Standard arithmetic (+,−,∗,/) and exponentiation.
- Elementary functions: sin, cos, log, exp.
- Finite sum and product notation: Converting `sum(n from start to end: expr)` into either loops or algebraic constants.
- Ability to define piecewise functions: `if-else` syntax may enable the user to define expressions differently based on
  various inputs.

2. Symbolic derivation engine - users can define functions and request derivatives with respect to specific variables. The compiler applies the chain
   rule and power rule recursively to generate the derivative expression before passing them on.

3. Optimization - that part includes:
- Common subexpression elimination: identifying repeated terms (like x2 or sin(y)) and assigning them to temporary
  variables (t0​,t1​) to prevent redundant calculations. That is done by converting expression parse tree into directed
  acyclic graph by merging nodes containing the same expressions.
- Constant folding: pre-calculating values that do not depend on input variables (e.g., the sum of 1…10 becomes 55).
- Identity reduction: eg. simplifying 0⋅x to 0 and 1⋅x to x

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

definition: IDENTIFIER "(" param_list? ")" ":=" expression ";" -> definition

param_list: IDENTIFIER ("," IDENTIFIER)* -> param_list

target: ">" expression "as" IDENTIFIER "(" param_w_type_list? ")" "->" TYPE ";" -> generate_target

param_w_type_list: TYPE IDENTIFIER ("," TYPE IDENTIFIER)* -> generate_param_with_type_list

?expression: "if" condition "then" expression ("elif" condition "then" expression)* "else" expression -> if_struct
           | expr

?condition: log_and ("or" log_and)* -> logic_or
?log_and: comparison ("and" comparison)* -> logic_and

?comparison: BOOL_CONST -> bool_const
           | expr REL_OP expr -> cond_op
           | "(" condition ")"

?expr: term (ADD_OP term)* -> add
?term: factor (MUL_OP factor)* -> prod
?factor: "-" factor -> negate
       | power
?power: atom ("^" power)? -> power

?atom: NUMBER -> float_num
     | IDENTIFIER -> variable
     | function_call
     | shorthand
     | derivative
     | "(" expression ")"

function_call: IDENTIFIER "(" arg_list? ")" -> function_call
arg_list: expr ("," expr)* -> arg_list

shorthand: SHORTHAND_TYPE "(" IDENTIFIER FROM INT TO INT ":" expression ")" -> shorthand
derivative: "diff" "(" IDENTIFIER "," INT "," expression ")" -> differentiate

BOOL_CONST.2: "true" | "false"

TYPE.2: "double" | "float" | "int"
REL_OP: "==" | "!=" | ">" | "<" | ">=" | "<="
MUL_OP: "*" | "/"
ADD_OP: "+" | "-"
SHORTHAND_TYPE.2: "sum" | "prod"
FROM.2: "from"
TO.2: "to"

%import common.CNAME -> IDENTIFIER
%import common.NUMBER
%import common.INT
%import common.WS
%ignore WS
```
## System Architecture
The engine is modularized across separate layers:

### Directory Structure
- **`based/parser/`**: Conducts text scanning, validation, and semantic translation rules.
  - `ScopeVisitor.py`: An interpreter subclass (`visitors.Interpreter`) executing **Static Scope Resolution and Semantic Verification**. It enforces namespace constraints by maintaining a stack of declaration scopes, catching conflicts or scoping violations at compile time (e.g., throwing `SemanticError`).
  - `TreeTransformer.py`: A `Transformer` implementation converting syntactical structural tree sequences directly into production mathematical/logic objects.
- **`based/Structure/`**: Contains the symbolic algebra core expressions (`Addition`, `Multiplication`, `Exponentiation`, `IfStructure`, logic comparison wrappers, and analytical trigonometric modifiers). 

### Semantic Code Validation
The `ScopeVisitor` enforces strict constraints prior to code generation:
1. **Namespace Isolation:** Detects duplicate function definitions or local loop parameter collisions in the current scope block.
2. **Undeclared Names:** Throws immediate errors if variables or local methods are invoked without matching contextual visibility declarations.
3. **Recursion Safeguards:** Inline user macros defined via assignment (`:=`) are strictly evaluated inline and **cannot be called recursively**. Recursion is permitted exclusively for declared explicit target blocks.
4. **Signature Constraints:** Asserts that arguments supplied to mathematical function structures or user-defined models match the absolute expected parameter length count exactly.

## User Guide

B.A.S.E.D. includes a command-line interface (`based_cli.py`). Instead of generating raw uncompiled textual strings, it directly maps expression formulas into production-ready `.so` files.

### Compilation Pipeline Breakdown
1. **Source Ingestion:** The program reads the `.based` formula source definition file into memory.
2. **Translation & Optimization:** The text undergoes parsing, semantic validation via `ScopeVisitor`, and macro expansion/symbolic reduction via `TreeTransformer`. 
3. **C Code Generation:** An intermediate C file named `<input_prefix>_codegen.c` is automatically generated, prepended with standard math imports (`#include <math.h>`).
4. **C Library Compilation:** The program triggers an out-of-process system execution loop using the host compiler engine (default: `gcc`). It creates a shared library linkage object (`-shared`).
5. **Output & Cleanup:** Generates the library and automatically removes the intermediate C source file unless preservation flags are explicitly set.

### CLI Options & Usage
```bash
python based_cli.py input.based [options]
```
- `input` – (Required) Path to the source file containing math functions and target definitions.
- `-o`, `--output` – Custom output name for the compiled library binary (defaults to <input_prefix>.so or <input_prefix>.dll).
- `--cc` – The backend C compiler executable toolchain to use (Default: gcc).
- `--keep-c` – Flag to preserve the intermediate <input_prefix>_codegen.c generated C source on disk for debugging or auditing instead of deleting it.

## Example
For input:
```
loss(w, x, y) := (1.0 / (1.0 + 2.71828 ^ (- (w * x)))) - y;
squared_error(w, x, y) := loss(w, x, y) ^ 2;

exp_taylor(x) := sum(i from 0 to 5 : (x ^ i) / fact(i));

cube_minus_target(x, target) := x ^ 3 - target;

newton_step(x, target) := x - cube_minus_target(x, target) / diff(x, 1, cube_minus_target(x, target));


> diff(w, 1, squared_error(w, x, y)) as compute_gradient(double w, double x, double y) -> double;


> if n <= 1 then 1.0 else n * fact(n - 1) as fact(int n) -> int;
> exp_taylor(val) as compile_exp(double val) -> double;

>   if iterations == 0 then
        guess
    else
        optimize_cbrt(newton_step(guess, radicand), radicand, iterations - 1)
as optimize_cbrt(double guess, double radicand, int iterations) -> double;```
```
The resulting C function could be:
```C
#include <math.h>

double compute_gradient(double w, double x, double y) {
    return (2 * (pow((1.0 + pow(2.71828, (-1 * (w * x)))), -1.0) - y) * (-1.0 * pow((1.0 + pow(2.71828, (-1 * (w * x)))), -2.0) * (pow(2.71828, (-1 * (w * x))) * (-1 * x))));
}

int fact(int n) {
    return ((n <= 1) ? (1.0) : (n * fact((n - 1))));
}

double compile_exp(double val) {
    return ((1.0 / fact(0)) + (val / fact(1)) + (pow(val, 2) / fact(2)) + (pow(val, 3) / fact(3)) + (pow(val, 4) / fact(4)) + (pow(val, 5) / fact(5)));
}

double optimize_cbrt(double guess, double radicand, int iterations) {
    return ((iterations == 0) ? (guess) : (optimize_cbrt((guess - ((pow(guess, 3) - radicand) / (3 * pow(guess, 2)))), radicand, (iterations - 1))));
}
```

## TODO

- [x] Project outline
- [x] Initial phase
    - [x] Grammar for LARK
    - [x] Token table
    - [x] Code structure
- [x] Basics of arithmetic engine
    - [x] Basic operations on constants
    - [x] Arithmetic operations on variables
    - [x] Simplification of arithmetic operations with variables
- [x] Extended mathematical engine
    - [x] Differentiation engine
    - [x] Basic mathematical functions implementation (e.g. sin, cos, ln, ...)
    - [x] Custom function definition (within `definition` tag)
        - [x] Ensure recursive functions work with if-else structure (probably after code generation done?)
    - [x] Shorthand for sum and product evaluation
- [x] Basic logic engine
    - [x] Constant logic conditions evaluation
    - [x] Logic expression to some normal form conversion
    - [x] Logic expression simplification
    - [x] If-else structure implementation
- [x] Syntax and semantics correctness
    - [x] Variable and function name scope control
    - [x] Syntax errors handling
    - [x] Semantic errors handling
- [x] C Code generation
    - [x] Basic code generation
    - [x] Common subexpression elimination
- [x] Simple command line interface
- [x] Add useful usage examples
