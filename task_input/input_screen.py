from kivy.properties import (
    ObjectProperty, StringProperty
 )
from kivy.uix.screenmanager import Screen
from libs.simplex_method.simplex_method import SimplexMethod, Sign, Extremum, SimplexMethodResult
from task_input.limitation_widget import LimitationWidget
from kivy.lang import Builder

Builder.load_file('task_input/input_screen.kv')


class InputScreen(Screen):
    f = StringProperty('')
    extremum = StringProperty('')
    limitations_list_layout = ObjectProperty(None)

    error_result = None

    def __init__(self, **kw):
        self.error_result = SimplexMethodResult.unknown()
        super().__init__(**kw)

    def calculate(self):
        # if we have limitations
        if len(self.limitations_list_layout.children) == 0:
            return

        # help function
        def sanitize_str(string: str):
            return string.strip().strip(';')

        # convert string to array of floats
        function = list(map(lambda el: float(el), sanitize_str(self.f).split(';')))

        # get extremum
        extremum = Extremum.from_string(self.extremum)

        # build conditions list
        conditions = []
        for i in range(len(self.limitations_list_layout.children)-1, -1, -1):
            limitation_widget = self.limitations_list_layout.children[i]
            # coefficients
            condition_coefficients = []
            condition_coefficients.extend(list(map(lambda el: float(el),
                                                   sanitize_str(limitation_widget.coefficients).split(';'))))
            condition_coefficients.append(float(sanitize_str(limitation_widget.free_coefficient)))
            # sign
            sign = Sign.from_string(sanitize_str(limitation_widget.sign))
            # add condition
            conditions.append((condition_coefficients, sign))

        sm = SimplexMethod.problem(function, conditions, extremum)
        sm_result = sm.calculate()

        return sm_result

    def add_limitation(self):
        self.limitations_list_layout.add_widget(LimitationWidget(size_hint=(1, None), height=60))

    def remove_last_limitation(self):
        layout = self.limitations_list_layout
        if len(layout.children) == 0:
            return
        layout.remove_widget(layout.children[0])