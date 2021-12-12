from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BooleanProperty


Builder.load_file('error/error_popup.kv')


class ErrorPopup(Popup):

    DEFAULT_TEXT = 'При работе приложения произошла неизвестная ошибка!'

    text = StringProperty(DEFAULT_TEXT)
    open_after_create = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.open_after_create:
            self.open()

    @staticmethod
    def error_checker(func):
        try:
            return func()
        except Exception as e:
            ErrorPopup(
                text='При работе приложения произошла ошибка!\nОписание:\n%s' % e,
                open_after_create=True
            )
