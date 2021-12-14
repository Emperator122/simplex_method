import numpy as np
from libs.simplex_method.simplex_method_result import SimplexMethodResult
from libs.simplex_method.task_enums import Extremum, Sign


class SimplexMethod:
    SKIP = float('inf')
    ITER_LIMIT = 9999999

    simplex_table = None
    simplex_basis_map = None
    simplex_top_map = None
    extremum = None
    f_index = None

    __method_result = None

    def __init__(self, simplex_table, simplex_basis_map, simplex_top_map, f_index, extremum=Extremum.MAX):
        self.simplex_table = simplex_table
        self.simplex_basis_map = simplex_basis_map
        self.simplex_top_map = simplex_top_map
        self.f_index = f_index
        self.extremum = extremum

    @classmethod
    def problem(cls, function, conditions, extremum=Extremum.MAX):
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

        return cls(simplex_table, simplex_basis_map, simplex_top_map, f_index, extremum)

    def calculate(self) -> SimplexMethodResult:
        try:
            result = self.__calculate()
            return result
        except AssertionError as e:
            if self.__method_result is None:
                return SimplexMethodResult.unknown(e)
            self.__method_result.error = True
            self.__method_result.error_message = e
            return self.__method_result

    def __calculate(self) -> SimplexMethodResult:
        """
        Calculates maximum of function using the source simplex table
        :return: SimplexMethodResult
        """
        simplex_basis_map = self.simplex_basis_map
        simplex_top_map = self.simplex_top_map
        simplex_1 = self.simplex_table

        # result var
        self.__method_result = SimplexMethodResult()
        method_result = self.__method_result
        method_result.extremum = self.extremum

        # check extremum type
        if self.extremum is Extremum.MIN:
            simplex_1[self.f_index, :] *= -1
        elif self.extremum is not Extremum.MAX:
            assert False, 'Wrong extremum value'

        iter_number = 0
        while iter_number <= self.ITER_LIMIT:
            # remove additional basis functions (if need)
            synthetics_count = len(simplex_basis_map) - 1 - self.f_index
            removed_count = 0
            for i in range(synthetics_count):
                # start from the end
                basis_index = len(simplex_basis_map) - 1 - i + removed_count
                header_index = len(simplex_top_map) - 2 - i + removed_count  # -2 because free_element

                # header without free element and synthetic variables
                check_interval = len(simplex_top_map) - 1 - synthetics_count
                if np.max(simplex_1[basis_index, :check_interval]) == 0:  # if we have only zeros on  check_interval
                    # remove variable and function from simplex table, basis_map and top_map
                    simplex_1 = np.delete(simplex_1, basis_index, axis=0)
                    simplex_1 = np.delete(simplex_1, header_index, axis=1)
                    simplex_top_map = np.delete(simplex_top_map, header_index)
                    simplex_basis_map = np.delete(simplex_basis_map, basis_index)
                    synthetics_count -= 1
                    removed_count += 1

            # stop condition
            if np.min(simplex_1[self.f_index, :len(simplex_top_map) - 1]) >= 0 and \
                    self.f_index == simplex_1.shape[0] - 1:
                break

            # relation column
            relation = np.repeat(self.SKIP, len(simplex_basis_map))

            # additional variable: index of the free element column
            free_ind = len(simplex_top_map) - 1

            # find main column
            main_column = SimplexMethod._get_main_column(simplex_1, self.f_index)

            # find relation
            for basis_index in range(self.f_index):
                if simplex_1[basis_index, free_ind] >= 0 and simplex_1[basis_index, main_column] > 0:
                    relation[basis_index] = simplex_1[basis_index, free_ind] / simplex_1[basis_index, main_column]

            # find main row
            main_row = SimplexMethod._get_main_row(relation, simplex_1, main_column)

            # add table to result
            method_result.add_simplex_table(
                header=np.r_[simplex_top_map, ['relation']],
                basis=simplex_basis_map.copy(),
                values=np.c_[simplex_1, relation],
                main_column_index=main_column,
                main_row_index=main_row,
            )

            # find and work with main element
            main_el = simplex_1[main_row, main_column]
            assert main_el != 0, 'main element 0'
            if main_el != 1:
                simplex_1[main_row, :] /= main_el

            # build next simplex table
            simplex_2 = np.zeros(simplex_1.shape) * 1.0
            simplex_2[main_row, :] = simplex_1[main_row, :]
            for basis_index in range(len(simplex_basis_map)):
                if basis_index == main_row:
                    continue
                simplex_2[basis_index, :] = simplex_1[basis_index, :] - simplex_1[basis_index, main_column] * simplex_1[main_row, :]
            simplex_1 = np.copy(simplex_2)

            # change basis
            simplex_basis_map[main_row] = simplex_top_map[main_column]

            assert relation.min() != self.SKIP, 'can\'t find any decision'
            iter_number += 1

        # fill and return result
        method_result.add_simplex_table(
            header=simplex_top_map,
            basis=simplex_basis_map,
            values=simplex_1,
        )
        # for min add additional simplex table
        if self.extremum is Extremum.MIN:
            temp = np.copy(simplex_1)
            temp[self.f_index, len(simplex_top_map) - 1] *= -1
            method_result.add_simplex_table(
                header=simplex_top_map,
                basis=simplex_basis_map,
                values=temp,
            )
            simplex_1 = temp

        method_result.result_free_elements = simplex_1[:, simplex_1.shape[1]-1]
        method_result.result_basis = simplex_basis_map
        return method_result

    @staticmethod
    def _get_main_column(simplex: np.ndarray, f_index) -> int:
        def get_min_indexes(array) -> np.ndarray:  # help function
            min_el = np.min(array)
            return np.argwhere(array == min_el)

        # if we have synthetic functions
        if f_index < simplex.shape[0]-1:
            # sum all synthetic functions
            temp = np.sum(simplex[f_index+1:simplex.shape[0], :simplex.shape[1] - 1], axis=0)
            min_indexes = get_min_indexes(temp)
            if len(min_indexes) == 1:  # if we have only one min_index then just return it
                return min_indexes[0][0]
            else:  # else find f values on these indexes and return minimum
                f_values = [simplex[f_index, i] for i in min_indexes]
                return min_indexes[get_min_indexes(f_values)[0][0]][0]

        # just find min value and return it
        min_indexes = get_min_indexes(simplex[f_index, :simplex.shape[1] - 1])
        return min_indexes[0][0]

    @staticmethod
    def _get_main_row(relation: np.ndarray, simplex: np.ndarray, main_column_index: int) -> int:
        def get_min_indexes(array) -> np.ndarray:  # help function
            min_el = np.min(array)
            return np.argwhere(array == min_el)

        min_indexes = get_min_indexes(relation)
        # if we find one min_index then return it
        if len(min_indexes) == 1:
            return min_indexes[0][0]

        # else use Bland's rule
        help_table = []
        help_table_rows = []
        for i_ in min_indexes:  # build help table
            i = i_[0]
            main_el = simplex[i, main_column_index]
            if main_el == 0:
                continue
            help_table.append((np.array([simplex[i, :]])/main_el)[0])
            help_table_rows.append(i)
        # find first row with min column value
        help_table = np.array(help_table)
        for j in range(help_table.shape[1]):
            temp_indexes = get_min_indexes(help_table[:, j])
            if len(temp_indexes) == 1:
                return help_table_rows[temp_indexes[0][0]]

        # else return first index
        return min_indexes[0][0]
