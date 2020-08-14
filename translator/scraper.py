# scraper.py

import requests
from bs4 import BeautifulSoup


class Translator:

    possible_tenses = [
        'presentIndicative',
        'preteritIndicative',
        'imperfectIndicative',
        'conditionalIndicative',
        'futureIndicative',
        'presentSubjunctive',
        'imperfectSubjunctive',
        'imperfectSubjunctive2',
        'futureSubjunctive',
        'imperative'
    ]

    def translate_word(self, word, tenses):

        for t in tenses:
            assert t in Translator.possible_tenses, "Invalid Tenses"

        # url
        path = "http://www.spanishdict.com/translate/" + word

        # user agent
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'

        # grabbing html
        html_raw = requests.get(path, headers=headers).content
        html = BeautifulSoup(html_raw, features="lxml")

        translation = html.find_all("div", attrs={"id": "quickdef1-es"})

        try:
            translation = translation[-1].get_text()

            if len(tenses) > 0 and html.find_all("div", "nav-content-item")[1].get_text() == "Conjugation":

                # conjugation url
                path = "http://www.spanishdict.com/conjugate/" + word

                # grabbing html
                html_raw = requests.get(path, headers=headers).content
                html = BeautifulSoup(html_raw, features="lxml")

                translation += "\n"
                for tense in tenses:
                    translation += "\n" + tense + ":" + "\n"
                    ts = html.find_all(
                        "a", attrs={"data-tense": tense})
                    for t in ts:
                        translation += t.get_text() + "\n"
        except IndexError:
            return "Unavailable"
        return translation

    def translate(self, words, t, a, b):
        # a, b are seperators
        s = ""
        translated_words = [self.translate_word(w, t) for w in words]
        for w, t in zip(words, translated_words):
            s += w + a + t + b
        return s

    def visual_translate(self, words, t, a, b):
        # a, b are seperators
        s = ""
        translated_words = []
        for w in words:
            tw = self.translate_word(w, t)
            print(w + ":\n" + tw)
            translated_words.append(tw)
        for w, t in zip(words, translated_words):
            s += w + a + t + b
        return s

    def translate_file(self, path, to_path, tenses, a=",", b=";", verbose=False):
        with open(path, "r") as w:
            words = w.read()
            w.close()
        words = words.split(",")
        words = [w.strip() for w in words]
        if verbose:
            translated_words = self.visual_translate(words, tenses, a, b)
        else:
            translated_words = self.translate(words, tenses, a, b)
        with open(to_path, "w") as tw:
            tw.write(translated_words)
            tw.close()
