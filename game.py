import re
import winsound
from functools import partial
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput


import constants as cst
import motus_api as api


from grid import *


def keep_blinking(instance, *args):
    instance.focus = True


def get_focus(text_input):
    Clock.schedule_once(partial(keep_blinking, text_input), .5)


class GameLayout(FloatLayout):

    my_text_input = ObjectProperty()
    my_grid = ObjectProperty()
    my_bt_validate = ObjectProperty()
    my_bt_replay = ObjectProperty()
    my_bt_settings = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)

        self.rows = cst.NB_LINES
        self.cols = 6

        Clock.schedule_once(self._init_later)

    def _init_later(self, *args):
        self.init_game()
        self.init_audio()
        self.my_text_input.bind(on_text_validate=self.on_text_validate)
        self.my_bt_replay.bind(on_press=self.on_press_replay)
        self.my_bt_validate.bind(on_press=self.on_bt_validate)

    def on_press_replay(self, widget):
        # delete textinput content
        self.my_text_input.text = ""
        self.init_game()

    def on_bt_validate(self, widget):
        self.on_text_validate(self.my_text_input)

    def init_game(self):
        # débloquer le textedit
        self.my_text_input.disabled = False

        # donner le focus au Text Edit
        get_focus(self.my_text_input)

        self.user_word = ""
        self.init_word_to_find()
        self.read_col = 0
        self.read_row = 0
        # tableau de booleens qui indique si une lettre est bien placée
        self.well_placed_letters = [0] * self.cols
        # on donne la première lettre
        self.well_placed_letters[0] = 1

        self.my_grid.init()

        # display the 1st letter
        self.my_grid.display_one_letter(self.word_to_find[0], 0, 0)

    def init_word_to_find(self):
        self.word_to_find = api.get_word(self.cols)
        # print(self.word_to_find)

    def init_audio(self):
        self.init_winsound()
        self.init_kivy_audio()

    def init_winsound(self):
        # WINSOUND
        # self.sound_letter = {}
        # for i in range(3):
        #     self.sound_letter[i] = os.path.join("sounds", f"sound_0{i}.wav")

        self.sound_letter = {x: f"sounds/sound_0{x}.wav" for x in range(3)}
        self.sound_win = "sounds/gagne.wav"
        self.sound_loose = "sounds/perdu.wav"

    def init_kivy_audio(self):

        self.sound_0 = SoundLoader.load("sounds/sound_00.wav")
        self.sound_1 = SoundLoader.load("sounds/sound_01.wav")
        self.sound_2 = SoundLoader.load("sounds/sound_02.wav")

        self.sound = {x: SoundLoader.load(f"sounds/sound_0{x}.wav") for x in range(3)}

        self.sound_0.volume = 1
        self.sound_1.volume = 1
        self.sound_2.volume = 1


    def on_text_validate(self, widget):
        self.user_word = widget.text
        # print(self.user_word)

        # vérifier len de max col
        if api.check_word_validation(self.user_word, self.cols):

            # afficher le mot
            self.my_grid.display(self.user_word, self.read_row)

            # comparer chaque lettre
            compare_list = api.compare(self.user_word, self.word_to_find)

            # mise à jour de self.liste_place_ok
            for i in range(self.cols):
                if compare_list[i] == 2:
                    self.well_placed_letters[i] = 1

            # remettre col à 0
            self.read_col = 0

            # afficher le feedback graphique
            self.display_check_word(compare_list)

            # vider l'entry
            widget.text = ""

            # donner le focus au Text Edit
            get_focus(widget)

    def display_check_word(self, compare_list, *largs):

        letter_code = compare_list[self.read_col]
        self.my_grid.display_check_letter(self.read_row, self.read_col, letter_code)
        winsound.PlaySound(self.sound_letter[letter_code], winsound.SND_ASYNC)
        # self.sound[letter_code].play()

        if self.read_col < (self.cols - 1):
            self.read_col += 1
            # Clock.schedule_once(lambda: self.display_check_word(compare_list), 5)
            Clock.schedule_once(partial(self.display_check_word, compare_list), .2)
        else:
            # comparaison terminée
            # si gagné
            if api.check_word(self.user_word, self.word_to_find):
                winsound.PlaySound(self.sound_win, winsound.SND_ASYNC)
                # bloquer le textedit
                self.my_text_input.disabled = True

            # nouvel essai : changer de ligne et afficher les bonnes lettres
            elif self.read_row < (self.rows - 1):
                self.read_row += 1
                self.my_grid.display_good_letters(self.well_placed_letters, self.read_row, self.word_to_find)

            else:
                # perdu
                winsound.PlaySound(self.sound_loose, winsound.SND_FILENAME)
                # afficher la réponse
                self.read_col = 0
                self.display_answer(self.read_row, self.word_to_find)

                # bloquer le textedit
                self.my_text_input.disabled = True

    def display_answer(self, *largs):

        self.my_grid.display_answer_letter(self.read_row, self.read_col, self.word_to_find)
        winsound.PlaySound(self.sound_letter[2], winsound.SND_ASYNC)
        if self.read_col < (self.cols - 1):
            self.read_col += 1
            Clock.schedule_once(self.display_answer, .2)


class MyTextInput(TextInput):

    nb_cols = NumericProperty()
    pat = re.compile('[^a-z]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if len(self.text) < self.nb_cols:
            s = re.sub(pat, '', substring)
            s = s.upper()
            return super(MyTextInput, self).insert_text(s, from_undo=from_undo)
        # else:
        #     print("trop grand")

    # def on_text_change(self, instance, value):
    #     print('The widget', instance, 'have:', value)


class MainBoxLayout(BoxLayout):
    pass


class InputBox(BoxLayout):
    my_textInput = ObjectProperty(None)


class BottomLayout(GridLayout):
    pass