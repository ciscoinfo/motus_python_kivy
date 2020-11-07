import os
import random
import string
import constants as cst


# Retourne la liste des mots à deviner
def import_words_list(nb_letters):

    if nb_letters == 5:
        file_name = cst.FILE_WORDS_5
    elif nb_letters == 6:
        file_name = cst.FILE_WORDS_6
    elif nb_letters == 7:
        file_name = cst.FILE_WORDS_7

    file_words = os.path.join(cst.DIR_WORDS, file_name)

    with open(file_words, "r", encoding='utf8') as f:
        words = f.read().splitlines()

    random.shuffle(words)
    return words


def get_word(nb_letters):
    return import_words_list(nb_letters)[0]

def check_word(user_word, word_to_find):
    return user_word == word_to_find


def check_word_validation(word, nb_char):
    # On vérifie qu'il y a au max self.NB_COLUMNS - 1 chars dans l'entry
    cond_1 = len(word) == nb_char
    # if not cond_1:
    #     print(f"Le mot ne contient pas {nb_char} caractères")
    # On vérife qu'on ajoute une lettre majuscule
    cond_2 = all([char in string.ascii_uppercase for char in word])
    # if not cond_2:
    #     print(f"Le mot ne contient pas que des lettres majuscules")
    res = cond_1 and cond_2
    return res

# initialise an array of booleans : liste des lettres bien placées
# the first position is 1-True - others are 0-False
def init_letters_ok(word_size):
    letters_ok = [0] * word_size
    letters_ok[0] = 1
    return letters_ok


# compare user_word and word_to_find
# return an array of int
# 0 : lettre absente
# 1 : lettre mal placée
# 2 : lettre bien placée
def compare(user_word, word_to_find):

    word_len = len(word_to_find)

    res = [0] * word_len

    # liste de booléens qui indique si une lettre a été parcourue
    # 1 non parcourue
    # 0 parcouru
    letters_read = [1] * word_len


    # 1st loop : looking for matching letters
    for i in range(word_len):
        if user_word[i] == word_to_find[i]:
            # well placed letter
            res[i] = 2
            # update letters_read
            letters_read[i] = 0

    # 2nd loop : looking for other letters
    for i in range(word_len):

        # vérifier que la lettre n'a pas déjà été ajoutée dans la boucle 1
        if user_word[i] != word_to_find[i]:

            for j in range(word_len):
                if user_word[i] == word_to_find[j] and letters_read[j] == 1:
                    # the letter is in the word but not well placed
                    res[i] = 1
                    # update letters_read
                    letters_read[j] = 0
                    break

    return res


if __name__ == '__main__':

    words = import_words_list()
    print(words)