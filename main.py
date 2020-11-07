import kivy
from kivy.app import App
from manager import *
kivy.require('1.11.1')


class MotusApp(App):

    def build(self):
        main = MyScreenManager()
        return main


if __name__ == '__main__':
    MotusApp().run()
