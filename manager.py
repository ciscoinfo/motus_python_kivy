from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from game import *
from settings import *


class MyScreenManager(ScreenManager):
    # Controller

    settings_layout = ObjectProperty()
    game_layout = ObjectProperty()

    screen_settings = ObjectProperty()
    screen_game = ObjectProperty()


    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

        Window.size = (515, 655)

        # first screen
        self.current = self.screen_settings.name

        # SCREEN SETTINGS

        self.bt_ok = self.settings_layout.bt_ok
        self.bt_ok.bind(on_press=self.on_press_bt)

        self.game_layout.my_bt_settings.bind(on_press=self.on_settings_press)

        # Window.bind(on_resize=self.track_size)


    # def track_size(self, instance, width, height):
    #     print(f"width : {width}")
    #     print(f"height : {height}")
    #     print(f"instance : {instance}")

    def on_press_bt(self, obj):
        # print(f"La valeur est : {self.settings_layout.get_counter()}")
        new_cols = self.settings_layout.get_counter()
        self.current = "screen_game"
        self.transition.direction = 'left'

        self.game_layout.my_grid.repopulate(new_cols)

        self.game_layout.my_text_input.nb_cols = new_cols

        self.game_layout.cols = new_cols

        self.set_window_size(new_cols)

        self.game_layout.init_game()

    def set_window_size(self, nb_cols):
        if nb_cols == 5:
            Window.size = (515, 735)
        elif nb_cols == 6:
            Window.size = (515, 655)
        elif nb_cols == 7:
            Window.size = (515, 595)

    def on_settings_press(self, obj):
        self.current = "screen_settings"
        self.transition.direction = 'right'