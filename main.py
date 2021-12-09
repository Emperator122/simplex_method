from libs.simplex_method.simplex_method import SimplexMethod, Sign

function = [1, 3]
conditions = [
    ([1, 1, 2], Sign.LEQ),
    ([2, 3, 6], Sign.GEQ),
]
sm2 = SimplexMethod.problem(function, conditions)
print(sm2.calculate())
