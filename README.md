# B.A.S.E.D. - Broad Arithmetic Symbolic Expression Derivator
B.A.S.E.D. is aimed to be a symbolic expression compiler designed to transform complex mathematical notation into optimized C code.
Authors:
- Antoni Kubiak antonikubiak@student.agh.edu.pl,
- Szymon Król szymonkrol@student.agh.edu.pl.

Mathematical expressions compiler
Result: C code
Implementation language: Python 3
Parser generator: Lark


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
- Finite sum and product notation: Converting `sum(n; start; end; expr)` into either loops or algebraic constants.
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
f(x) := x+2
g(x, y) := x^2+sin(y) + 1
> f(x) + 2*g(x, x) + sin(x); foo; double
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
> sum(n; 1; 10; n*x^2); foo; double
```
The resulting C function could be:
``` C
double foo(x) {
	return 55*x*x;
}
```
