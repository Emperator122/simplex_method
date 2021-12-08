import numpy as np
from libs.simplex_method.simplex_method import SimplexMethod, Sign

function = [2, 2]
conditions = [
    ([1, 1, 3], Sign.LEQ),
    ([1, 0, 1], Sign.GEQ),
]
sm2 = SimplexMethod.problem(function, conditions)
print(sm2.calculate())
