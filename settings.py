from kivy.clock import Clock
from kivy.properties import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.widget import Widget

import constants as cst


class TriangleButtonRight(ButtonBehavior, Widget):
    def collide_point(self, x, y):
        x0 = self.x
        y0 = self.y
        x1 = x0 + self.width
        y1 = y0 + self.height / 2
        y2 = y0 + self.height
        a1 = (y0 - y1) / (x0 - x1)
        a2 = (y2 - y1) / (x0 - x1)

        collide_inf = False
        collide_border = False
        collide_sup = False

        if y >= a1 * x + y0 - x0 * a1:
            collide_inf = True

        if x >= x0:
            collide_border = True

        if y <= a2 * x + y2 - a2 * x0:
            collide_sup = True

        return all([collide_inf, collide_border, collide_sup])


class TriangleButtonLeft(ButtonBehavior, Widget):
    def collide_point(self, x, y):
        x0 = self.x
        y0 = self.y
        x1 = x0 + self.width
        y1 = y0 + self.height / 2
        y2 = y0 + self.height

        a1 = (y1 - y2) / (x0 - x1)
        a2 = (y1 - y0) / (x0 - x1)

        collide_inf = False
        collide_border = False
        collide_sup = False

        if y >= a2 * x + y1 - a2 * x0:
            collide_inf = True
        if x <= x1:
            collide_border = True
        if y <= a1 * x + y1 - x0 * a1:
            collide_sup = True

        return all([collide_inf, collide_border, collide_sup])


class SettingsFloatLayout(FloatLayout):
    # pass
    bt_backward = ObjectProperty()
    bt_forward = ObjectProperty()
    lb_counter = ObjectProperty()

    def __init__(self, **kwargs):
        super(SettingsFloatLayout, self).__init__(**kwargs)

        Clock.schedule_once(self._init_later)
        self.counter = 6

    def _init_later(self, *args):
        self.bt_backward.bind(on_press=self.bt_backward_press)
        self.bt_forward.bind(on_press=self.bt_forward_press)
        self.update_counter()

    def bt_backward_press(self, instance):
        if self.counter > cst.COUNTER_MIN:
            self.counter -= 1
        self.update_counter()

    def bt_forward_press(self, instance):
        if self.counter < cst.COUNTER_MAX:
            self.counter += 1
        self.update_counter()

    def update_counter(self):
        self.lb_counter.text = f"{self.counter}"

    def get_counter(self):
        return self.counter
