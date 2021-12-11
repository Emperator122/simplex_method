from libs.simplex_method.simplex_method import SimplexMethod, Sign, Extremum

function = [1, 3]
conditions = [
    ([1, 1, 2], Sign.LEQ),
    ([2, 3, 6], Sign.GEQ),
]

# function = [-6, 4, 4]
# conditions = [
#     ([-3, -1, 1, 2], Sign.GEQ),
#     ([-2, -4, 1, 3], Sign.GEQ),
# ]
# P.S. MAX
sm = SimplexMethod.problem(function, conditions, Extremum.MAX)
sm_result = sm.calculate()
print(sm_result)
if sm_result is not None:
    for matrix in sm_result.simplex_tables:
        print(matrix)

