from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file('task_input/dropdown_widgets.kv')


class SignDropDown(BoxLayout):
    selected_value = StringProperty('?')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'


class ExtremumDropDown(BoxLayout):
    selected_value = StringProperty('max')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
