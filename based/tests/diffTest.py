from based.Structure.Expressions.Variable import Variable
from based.Structure.Expressions.Functions.Sin import Sin

x = Variable.create("x")
expr = x * Sin.create(x)

derivative = expr.diff("x")
print(f"Oryginał: {expr}")
print(f"Pochodna: {derivative}")
