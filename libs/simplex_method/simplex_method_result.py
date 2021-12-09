import numpy as np


class SimplexMethodResult:
    simplex_tables = []
    result_free_elements = None
    result_basis = None
    error = False
    error_message = None

    @property
    def iter_count(self):
        return len(self.simplex_tables)

    def add_simplex_table(self, header, basis, values, main_row_index=-1, main_column_index=-1):
        self.simplex_tables.append(
            SimplexTable(header, basis, values, main_row_index, main_column_index)
        )

    def __str__(self):
        description = 'SimplexMethodResult\r\nError: %s;\r\n' % self.error
        if self.error:
            description += 'Error description:\r\n"%s";' % self.error_message
        description += 'Basis is:\t\t%s;\r\nFree elements:\t%s.' % (self.result_basis, self.result_free_elements)
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
                description += '%-12s' % self.values[i, j]
            description += '\r\n'

        return description
