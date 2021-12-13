from libs.simplex_method.simplex_method import SimplexMethod, Sign, Extremum


sm_result = SimplexMethod.problem(
            function=[5,8,6],
            conditions=[
                ([5,5,2,1200], Sign.LEQ),
                ([4,0,3,300], Sign.LEQ),
                ([0,2,4,800], Sign.LEQ),
            ],
            extremum=Extremum.MAX
        ).calculate()
print(sm_result)
if sm_result is not None:
    for matrix in sm_result.simplex_tables:
        print(matrix)

