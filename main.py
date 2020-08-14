# main.py
# main spqa file

import os
from translator.scraper import Translator

t = Translator()

print("Welcome to the Spanish Quizlet Automater. \n")
print("Please place all the words you would like to have translated in the file 'words.txt' located in the translator folder. \n")
print("Please use commas to seperate each sequence you would like translaed.")
print("i.e. comer, me llamo, hola, etc... \n")

tenses = []
for tense in Translator.possible_tenses:
    q = input("Would you like to include the " + tense +
              " conjugations of your verb? (y/n/exit) ").lower().strip()
    if q == "y":
        tenses.append(tense)
    elif q == "exit":
        break

from_path = os.getcwd() + "/translator/words.txt"
to_path = os.getcwd() + "/translator/translated_words.txt"

print("\nTranslation commencing:")
t.translate_file(from_path, to_path, tenses, verbose=True)
print("The translation has been completed, please copy and paste the contents of 'translated_words.txt' in the translator folder and import them into your quizlet with comma and semi colon set as your seperators.")
