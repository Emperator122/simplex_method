from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import (
    NumericProperty, ColorProperty, ObjectProperty
 )


Builder.load_file('simplex_table_output/simplex_table.kv')


class BorderedLabel(Label):
    DEFAULT_COLOR = [0, 1, 0, 1]

    border_color = ColorProperty(DEFAULT_COLOR)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SimplexTableGrid(GridLayout):
    current_index = NumericProperty(0)
    sm_result = ObjectProperty(None)
    count = NumericProperty(0)

    @property
    def has_next(self) -> bool:
        return self.current_index + 1 < len(self.sm_result.simplex_tables)

    @property
    def has_previous(self) -> bool:
        return self.current_index - 1 >= 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_table(self, table_index=0):
        def add_column(text, text_color=None):
            if text_color is None:
                self.add_widget(BorderedLabel(text=text))
            else:
                self.add_widget(BorderedLabel(text=text, color=text_color))
        self.clear_widgets()
        table = self.sm_result.simplex_tables[table_index]
        self.cols = table.values.shape[1] + 1
        # header
        add_column('/')
        for item in table.header:
            add_column(str(item))

        for i in range(len(table.basis)):
            basis_item = table.basis[i]
            add_column(str(basis_item))
            for j in range(table.values.shape[1]):
                # select color
                color = None
                if j == table.main_column and i == table.main_row:
                    color = [1, 0, 1, 1]
                elif i == table.main_row:
                    color = [1, 0, 0, 1]
                elif j == table.main_column:
                    color = [0, 0, 1, 1]

                add_column('%.3f' % table.values[i, j], color)

    def load_next(self):
        if not self.has_next:
            return
        self.current_index += 1
        self.build_table(table_index=self.current_index)

    def load_previous(self):
        if not self.has_previous:
            return
        self.current_index -= 1
        self.build_table(table_index=self.current_index)

    def on_sm_result(self, instance, value):
        if self.sm_result is not None:
            self.count = len(self.sm_result.simplex_tables)
            self.build_table(table_index=self.current_index)
