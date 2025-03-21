from sympy import Symbol

x = Symbol('x', positive=True)
if (x + 5) > 0:
    print('Do something')
else:
    print('Do something else')