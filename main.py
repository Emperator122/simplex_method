from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from kivy.lang import Builder
import os, sys
from kivy.resources import resource_add_path


class Navigator(ScreenManager):
    input_screen = ObjectProperty(None)
    simplex_tables_screen = ObjectProperty(None)

    def open_screen(self, name, attributes: dict = None):
        target_screen = self.get_screen(name)
        if attributes is not None:
            for attr_name, attr_value in attributes.items():
                setattr(target_screen, attr_name, attr_value)
        self.current = name


class SimplexMethodApp(App):
    def build(self):
        self.title = 'Симплек метод'
        return Navigator(transition=WipeTransition())


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    Builder.load_file('navigator.kv')
    SimplexMethodApp().run()
