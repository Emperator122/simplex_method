from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_file('simplex_table_output/simplex_table_screen.kv')


class SimplexTableScreen(Screen):
    sm_result = ObjectProperty(None)
