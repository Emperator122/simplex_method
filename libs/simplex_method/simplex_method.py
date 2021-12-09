from enum import IntEnum
import numpy as np


class Sign(IntEnum):
    LEQ = 3
    EQ = 2
    GEQ = 1


class SimplexMethod:
    skip = float('inf')
    ITER_LIMIT = 9999999

    simplex_table = None
    simplex_basis_map = None
    simplex_top_map = None
    f_index = None

    def __init__(self, simplex_table, simplex_basis_map, simplex_top_map, f_index):
        self.simplex_table = simplex_table
        self.simplex_basis_map = simplex_basis_map
        self.simplex_top_map = simplex_top_map
        self.f_index = f_index

    @classmethod
    def problem(cls, function, conditions):
        function = np.array(function)

        clean_conditions = []
        conditions_free_elements = []
        conditions_signs = []
        leq_count = 0
        geq_count = 0
        eq_count = 0
        for condition in conditions:
            clean_conditions.append(condition[0][:len(condition[0])-1])
            conditions_free_elements.append(condition[0][len(condition[0])-1])
            conditions_signs.append(condition[1])
            if condition[1] is Sign.GEQ:
                geq_count += 1
            elif condition[1] is Sign.LEQ:
                leq_count += 1
            else:
                eq_count += 1

        # help function
        def remove_zero_columns(arr: np.ndarray):
            idx = np.argwhere(np.all(arr[..., :] == 0, axis=0))
            return np.delete(arr, idx, axis=1)

        # lengths
        conditions_count = len(clean_conditions)
        default_vars_count = len(clean_conditions[0])
        # build the simplex table
        simplex_table = np.zeros((conditions_count+1+geq_count+eq_count, default_vars_count+2*conditions_count+1))
        # add default conditions and function ([0:conditions_count+1, default_vars_count] used)
        simplex_table[0:conditions_count, 0:default_vars_count] = clean_conditions
        simplex_table[conditions_count, 0:default_vars_count] = function*-1
        # add new basis variables to top
        diag_matrix = np.eye(conditions_count)
        operators_matrix = \
            np.array([list(map(lambda sign: int(sign)-2, conditions_signs))]).T  # [-1 for GEQ, 1 for LEQ, 0 for GEQ]^T
        diag_operators_matrix = diag_matrix * operators_matrix
        simplex_table[0:conditions_count, default_vars_count:default_vars_count+conditions_count] = \
            diag_operators_matrix

        # add synthetic variables to top
        if geq_count+eq_count > 0:
            diag_matrix = np.eye(conditions_count)
            diag_operators_matrix = diag_matrix * np.abs(operators_matrix-2)//2
            simplex_table[0:conditions_count, default_vars_count+conditions_count:default_vars_count+2*conditions_count] \
                = diag_operators_matrix
        # add free element
        simplex_table[0:conditions_count, simplex_table.shape[1]-1] = conditions_free_elements
        # add synthetic functions
        i = 0  # current sign number var
        j = 0  # current geq number var
        for sign in conditions_signs:
            if sign is Sign.LEQ:
                i += 1
                continue
            simplex_table[conditions_count + 1 + j, :] = simplex_table[i, :] * -1
            simplex_table[conditions_count + 1 + j, default_vars_count+leq_count+geq_count+i] = 0
            i += 1
            j += 1
        simplex_table = remove_zero_columns(simplex_table)

        # form basis map
        simplex_basis_map = []
        for i in range(len(conditions_signs)):
            if conditions_signs[i] is Sign.LEQ:
                simplex_basis_map.append("x_%s" % str(default_vars_count + i + 1))
        simplex_basis_map.extend(["r_%s" % str(i + 1) for i in range(geq_count+eq_count)])
        simplex_basis_map.append("f")
        simplex_basis_map.extend(["W_%s" % str(i + 1) for i in range(geq_count+eq_count)])

        # form top map
        simplex_top_map = ["x_%s" % str(i + 1) for i in range(default_vars_count+leq_count+geq_count)]
        simplex_top_map.extend(["r_%s" % str(i + 1) for i in range(geq_count+eq_count)])
        simplex_top_map.append("free")

        # f_index
        f_index = conditions_count

        return cls(simplex_table, simplex_basis_map, simplex_top_map, f_index)

    def calculate(self):
        simplex_basis_map = self.simplex_basis_map
        simplex_top_map = self.simplex_top_map
        simplex_1 = self.simplex_table

        iter_number = 0
        while iter_number <= self.ITER_LIMIT:
            relation = np.repeat(self.skip, len(simplex_basis_map))
            free_ind = len(simplex_top_map) - 1

            # find main column
            main_column = SimplexMethod._get_main_column(simplex_1)

            # find relation
            for i in range(len(relation)):
                val = self.skip
                if simplex_1[i, free_ind] > 0 and simplex_1[i, main_column] > 0:
                    val = simplex_1[i, free_ind] / simplex_1[i, main_column]
                relation[i] = val

            # find main row
            main_row = SimplexMethod._get_main_row(relation)

            # find and work with main element
            main_el = simplex_1[main_row, main_column]
            assert main_el != 0, 'main element 0'
            if main_el != 1:
                simplex_1[main_row, :] /= main_el

            # build next simplex table
            simplex_2 = np.zeros(simplex_1.shape) * 1.0
            simplex_2[main_row, :] = simplex_1[main_row, :]
            for i in range(len(simplex_basis_map)):
                if i == main_row:
                    continue
                simplex_2[i, :] = simplex_1[i, :] - simplex_1[i, main_column] * simplex_1[main_row, :]
            simplex_1 = np.copy(simplex_2)

            # change basis
            simplex_basis_map[main_row] = simplex_top_map[main_column]

            # remove additional basis functions
            for i in range(len(simplex_basis_map) - 1, self.f_index, -1):
                if np.min(simplex_1[i, :len(simplex_top_map) - 1]) >= 0:
                    simplex_1 = np.delete(simplex_1, i, axis=0)
                    simplex_1 = np.delete(simplex_1, len(simplex_top_map) - 2, axis=1)
                    simplex_top_map = np.delete(simplex_top_map, len(simplex_top_map) - 1)
                    simplex_basis_map = np.delete(simplex_basis_map, len(simplex_basis_map) - 1)

            # stop condition
            if np.min(simplex_1[self.f_index, :len(simplex_top_map) - 1]) >= 0:
                break

            assert relation.min() != self.skip, 'can\'t find any decision'
            iter_number += 1

        print(simplex_basis_map)
        return simplex_1[:, simplex_1.shape[1]-1]

    @staticmethod
    def _get_main_column(simplex: np.ndarray) -> int:
        arg_min_last_row = simplex[simplex.shape[0] - 1, :simplex.shape[1] - 1].argmin()
        return arg_min_last_row

    @staticmethod
    def _get_main_row(relation: np.ndarray) -> int:
        arg_min = relation.argmin()
        return arg_min