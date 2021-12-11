from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('task_input/limitation_widget.kv')


class LimitationWidget(BoxLayout):
    coefficients = StringProperty('')
    sign = StringProperty('?')
    free_coefficient = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
