from libs.simplex_method.simplex_method import SimplexMethod, Sign, Extremum


sm_result = SimplexMethod.problem(
            function=[1, 3],
            conditions=[
                ([1, 1, 2], Sign.LEQ),
                ([2, 3, 6], Sign.GEQ),
            ],
            extremum=Extremum.MAX
        ).calculate()
print(sm_result)
if sm_result is not None:
    for matrix in sm_result.simplex_tables:
        print(matrix)

