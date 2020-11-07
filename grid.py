from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

import constants as cst
import utils


class MainGrid(GridLayout):

    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)

        self.cols = 6
        self.rows = cst.NB_LINES
        self.labels_rows = []
        self.populate()

    def populate(self):

        for i in range(self.rows):
            label_line = []
            for j in range(self.cols):
                new_label = CustomLabel()
                label_line.append(new_label)
                # afficher le label
                self.add_widget(new_label)

            # ajouter la ligne de labels
            self.labels_rows.append(label_line)

    def init(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.labels_rows[i][j].init()

    def display(self, word, row):
        for i in range(self.cols):
            self.labels_rows[row][i].text = word[i]

    def display_check_letter(self, row, col, check_code):

        label = self.labels_rows[row][col]
        label.change_mode(check_code)

    def display_one_letter(self, letter, row, col):

        label = self.labels_rows[row][col]
        label.text = letter

    def display_good_letters(self, well_placed_letters, num_line, word):

        # afficher les lettres bien placées
        for i in range(self.cols):
            if (well_placed_letters[i]):
                self.labels_rows[num_line][i].text = word[i]

    def display_answer_letter(self, row, col, word):

        # afficher une lettre bien placée à la position row col
        label = self.labels_rows[row][col]
        label.change_mode(2)
        self.labels_rows[row][col].text = word[col]

    def repopulate(self, cols):

        self.clear_widgets()
        self.cols = cols
        self.labels_rows = []

        for i in range(self.rows):
            label_line = []
            for j in range(self.cols):
                new_label = CustomLabel()
                label_line.append(new_label)
                # afficher le label
                self.add_widget(new_label)

            # ajouter la ligne de labels
            self.labels_rows.append(label_line)

class CustomLabel(Label):
    bg_color = ListProperty()
    bg_color_2 = ListProperty()

    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        self.mode = 0

        self.font_family = "Courrier"
        self.font_size = dp(50)
        self.bg_color = utils.rgb_to_kvColor(cst.BG_CELL_COLOR)
        self.bg_color_2 = cst.TRANSPARENT

    def change_mode(self, mode):
        # self.canvas.before.clear()
        self.mode = mode
        if mode == 0:
            self.bg_color = utils.rgb_to_kvColor(cst.BG_CELL_COLOR)
            self.bg_color_2 = cst.TRANSPARENT

        elif mode == 1:
            self.bg_color = utils.rgb_to_kvColor(cst.BG_CELL_COLOR)
            self.bg_color_2 = utils.rgb_to_kvColor(cst.BG_CELL_COLOR_ORANGE)

        else:
            self.bg_color = utils.rgb_to_kvColor(cst.BG_CELL_COLOR_RED)
            self.bg_color_2 = cst.TRANSPARENT

    def init(self):
        self.text = ""
        self.change_mode(0)
