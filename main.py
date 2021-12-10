from kivy.app import App
from kivy.uix.widget import Widget
from libs.simplex_method.simplex_method import SimplexMethod, Sign
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
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
    coefficients = ObjectProperty(None)
    sign = ObjectProperty(None)
    free_coefficient = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'


class InputScreen(Screen):
    f = ObjectProperty(None)
    limitations = ObjectProperty([])

    def calculate(self):
        function = [1, 3]
        conditions = [
            ([1, 1, 2], Sign.LEQ),
            ([2, 3, 6], Sign.GEQ),
        ]
        sm = SimplexMethod.problem(function, conditions)
        sm_result = sm.calculate()
        return sm_result


class PongApp(App):
    def build(self):
        #SimplexTableScreen(sm_result=sm_result)
        return Navigator(transition=WipeTransition())


if __name__ == '__main__':
    PongApp().run()
