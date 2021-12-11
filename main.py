from kivy.app import App
from kivy.uix.widget import Widget
from libs.simplex_method.simplex_method import SimplexMethod, Sign
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
 )
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, WipeTransition


class Navigator(ScreenManager):
    input_screen = ObjectProperty(None)
    simplex_tables_screen = ObjectProperty(None)

    sm_result = ObjectProperty(None)

    def open_screen(self, name, attributes: dict = None):
        target_screen = self.get_screen(name)
        if attributes is not None:
            for attr_name, attr_value in attributes.items():
                setattr(target_screen, attr_name, attr_value)
        self.current = name


class SimplexTableScreen(Screen):
    sm_result = ObjectProperty(None)


class LimitationWidget(BoxLayout):
    coefficients = StringProperty('')
    sign = StringProperty('?')
    free_coefficient = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'


class SignDropDown(BoxLayout):
    selected_value = StringProperty('?')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'


class InputScreen(Screen):
    f = StringProperty('')
    limitations_list_layout = ObjectProperty(None)

    def calculate(self):
        # function = [1, 3]
        # conditions = [
        #     ([1, 1, 2], Sign.LEQ),
        #     ([2, 3, 6], Sign.GEQ),
        # ]

        # if we have limitations
        if len(self.limitations_list_layout.children) == 0:
            return

        # help function
        def sanitize_str(string: str):
            return string.strip().strip(';')

        # convert string to array of floats
        function = list(map(lambda el: float(el), sanitize_str(self.f).split(';')))

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

        sm = SimplexMethod.problem(function, conditions)
        sm_result = sm.calculate()
        return sm_result

    def add_limitation(self):
        self.limitations_list_layout.add_widget(LimitationWidget(size_hint=(1, None), height=60))

    def remove_last_limitation(self):
        layout = self.limitations_list_layout
        if len(layout.children) == 0:
            return
        layout.remove_widget(layout.children[0])


class PongApp(App):
    def build(self):
        #SimplexTableScreen(sm_result=sm_result)
        return Navigator(transition=WipeTransition())


if __name__ == '__main__':
    PongApp().run()
