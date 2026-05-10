from based.Structure.Variable import Variable
from based.Structure.Sin import Sin

x = Variable.create("x")
expr = x * Sin.create(x)

derivative = expr.diff("x")
print(f"Oryginał: {expr}")
print(f"Pochodna: {derivative}")