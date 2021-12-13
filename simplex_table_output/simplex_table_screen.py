from kivy.uix.screenmanager import Screen
from kivy.uix.bubble import Bubble
from kivy.properties import ObjectProperty, StringProperty, Property
from kivy.lang import Builder


Builder.load_file('simplex_table_output/simplex_table_screen.kv')


class SimplexTableScreen(Screen):
    sm_result = ObjectProperty(None)
    error_bubble_box = ObjectProperty(None)

    def on_sm_result(self, instance, value):
        self.error_bubble_initialize()

    def error_bubble_initialize(self, show_error=True):
        self.error_bubble_box.clear_widgets()
        if show_error and self.sm_result.error:
            self.error_bubble_box.size_hint = (0.5, 1)
            self.error_bubble_box.add_widget(
                ErrorBubble(
                    error_text='При вычислении произошла следующая ошибка:\r\n%s\r\nНажмите для закрытия уведомления'
                               % self.sm_result.error_message,
                    on_tap=self.error_bubble_initialize
                )
            )
        else:
            self.error_bubble_box.size_hint = (None, None)
            self.error_bubble_box.height = 0


class ErrorBubble(Bubble):
    on_tap = None
    error_text = StringProperty('Неизвестная ошибка')

    def __init__(self, **kwargs):
        self.on_tap = kwargs.pop('on_tap')
        super().__init__(**kwargs)
