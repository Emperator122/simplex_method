import unittest
from libs.simplex_method.simplex_method import Extremum, Sign, SimplexMethodResult, SimplexMethod
import numpy as np


class SimplexMethodTasks(unittest.TestCase):
    def test_task_1(self):
        result = SimplexMethod.problem(
            function=[1, 3],
            conditions=[
                ([1, 1, 2], Sign.LEQ),
                ([2, 3, 6], Sign.GEQ),
            ],
            extremum=Extremum.MAX
        ).calculate()

        true_result = SimplexMethodResult()
        true_result.result_basis = ['x_4', 'x_2', 'f']
        true_result.result_free_elements = [0., 2., 6.]
        true_result.error = False
        true_result.extremum = Extremum.MAX

        self.assertTrue(SimplexMethodTasks.__results_equals(result, true_result))

    def test_task_2(self):
        result = SimplexMethod.problem(
            function=[-6, 4, 4],
            conditions=[
                ([-3, -1, 1, 2], Sign.GEQ),
                ([-2, -4, 1, 3], Sign.GEQ),
            ],
            extremum=Extremum.MIN
        ).calculate()

        true_result = SimplexMethodResult()
        true_result.result_basis = ['x_3', 'x_4', 'f']
        true_result.result_free_elements = [3.,  1., 12.]
        true_result.extremum = Extremum.MIN

        self.assertTrue(SimplexMethodTasks.__results_equals(result, true_result))

    def test_task_3(self):
        result = SimplexMethod.problem(
            function=[-1, 2],
            conditions=[
                ([1, 1, 2], Sign.LEQ),
                ([2, 1, 1], Sign.GEQ),
            ],
            extremum=Extremum.MAX
        ).calculate()

        true_result = SimplexMethodResult()
        true_result.result_basis = ['x_4', 'x_2', 'f']
        true_result.result_free_elements = [1., 2., 4.]
        true_result.extremum = Extremum.MAX

        self.assertTrue(SimplexMethodTasks.__results_equals(result, true_result))

    def test_task_4(self):  # one task, different conditions order
        result = SimplexMethod.problem(
            function=[-1, 2],
            conditions=[
                ([1, 1, 2], Sign.LEQ),
                ([2, 1, 1], Sign.GEQ),
            ],
            extremum=Extremum.MAX
        ).calculate()

        another_result = SimplexMethod.problem(
            function=[-1, 2],
            conditions=[
                ([2, 1, 1], Sign.GEQ),
                ([1, 1, 2], Sign.LEQ),
            ],
            extremum=Extremum.MAX
        ).calculate()

        result.result_free_elements = np.sort(result.result_free_elements)
        another_result.result_free_elements = np.sort(another_result.result_free_elements)

        result.result_basis = another_result.result_basis

        self.assertTrue(SimplexMethodTasks.__results_equals(result, another_result))

    def test_task_5(self):
        result = SimplexMethod.problem(
            function=[3, 2, 1],
            conditions=[
                ([0, 1, 1, 4], Sign.GEQ),
                ([2, 1, 2, 6], Sign.GEQ),
                ([2, -1, 2, 2], Sign.GEQ),
            ],
            extremum=Extremum.MIN
        ).calculate()

        true_result = SimplexMethodResult()
        true_result.result_basis = ['x_5', 'x_6', 'x_3', 'f']
        true_result.result_free_elements = [2.0000000000000004, 6., 4., 4.]
        true_result.extremum = Extremum.MIN

        self.assertTrue(SimplexMethodTasks.__results_equals(result, true_result))

    @staticmethod
    def __results_equals(result_1: SimplexMethodResult, result_2: SimplexMethodResult) -> bool:
        props = [
            np.all(result_1.result_basis == result_2.result_basis),
            np.all(result_1.result_free_elements == result_2.result_free_elements),
            result_1.error == result_2.error,
            result_1.extremum == result_2.extremum,
        ]
        return np.all(props)


if __name__ == '__main__':
    unittest.main()
