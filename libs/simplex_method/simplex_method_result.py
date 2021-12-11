import numpy as np
from libs.simplex_method.task_enums import Extremum


class SimplexMethodResult:
    simplex_tables = []
    result_free_elements = []
    result_basis = []
    error = False
    error_message = None
    extremum = Extremum.UNKNOWN

    @property
    def iter_count(self):
        return len(self.simplex_tables)

    @classmethod
    def unknown(cls, error_message='Unknown error'):
        result = cls()
        result.error = True
        result.error_message = error_message
        return result

    def add_simplex_table(self, header, basis, values, main_row_index=-1, main_column_index=-1):
        self.simplex_tables.append(
            SimplexTable(header, basis, values, main_row_index, main_column_index)
        )

    def __str__(self):
        description = 'SimplexMethodResult\r\nError: %s;\r\n' % self.error
        if self.error:
            description += 'Error description:\r\n"%s";' % self.error_message
        description += 'Basis is:\t\t%s;\r\nFree elements:\t%s.\r\n' % (self.result_basis, self.result_free_elements)
        if self.extremum is Extremum.MIN and not self.error:
            description += 'Because you searching MIN additional simplex table was added. result_free_elements ' \
                           'contains f multiplied by -1.\r\n'
        return description


class SimplexTable:
    header = None
    basis = None
    values = None
    main_row = None
    main_column = None

    def __init__(self, header, basis, values: np.ndarray, main_row_index, main_column_index):
        assert len(values) > 0, 'values is empty'
        assert len(header) == len(values[0]), 'rows size error'
        assert len(basis) == len(values), 'columns size error'

        self.header = header
        self.basis = basis
        self.values = values
        self.main_row = main_row_index
        self.main_column = main_column_index

    def __str__(self):
        # build header
        description = '%-12s' % '\\'
        for item in self.header:
            description += '%-12s' % item
        description += '\r\n'
        # build body
        for i in range(len(self.basis)):
            basis_item = self.basis[i]
            description += '%-12s' % basis_item
            for j in range(self.values.shape[1]):
                description += '%-12f' % self.values[i, j]
            description += '\r\n'

        return description
