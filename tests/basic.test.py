#!/usr/bin/env python3
from visual_novel.interpreter import getChoices, getDialogue, getBackground, getDescription, getHistory
import unittest


class BasicTests(unittest.TestCase):
    def test_getChoices(self):
        u"""Test la fonction getChoice de façon normale :
        avec deux choix et deux fichiers de sortie
        Le test s'attendent au résultat attendu pour pouvoir
        interpréter correctement l'histoire par le GUI
        """

        testTxt = '#No~dewit.txt|...~tragedy.txt$'
        expectOutput = {"type": "choice", "choice1": (
            'No', 'dewit.txt'), "choice2": ('...', 'tragedy.txt')}
        result = getChoices(testTxt)
        self.assertDictEqual(result, expectOutput)

    def test_getDialogue_without_chr_img(self):
        u"""Test la fonction getDialogue sans avoir inclue d'image pour le personnage
        Le message de base est une ligne de dialogue type pouvant être mise dans le script
        Le résultat attendu est un dictionnaire utilisable par l'interpréteur.
        """

        testTxt = "-Obiwan Kenobi@: -Hello there"
        expectOutput = {"type": "dialogue", "name": "Obiwan Kenobi",
                        "image": '', "text": "Hello there"}
        result = getDialogue(testTxt)
        self.assertDictEqual(result, expectOutput)

    def test_getDialogue_with_chr_img(self):
        u"""Test la fonction getDialogue en ayant inclue une image pour le personnage 
        ainsi que sa position (left ou right) sur le GUI
        Le message de base est une ligne de dialogue type pouvant être mise dans le script 
        Le résultat attendu est un dictionnaire utilisable par l'interpréteur"""

        testTxt = "-Obiwan Kenobi@truejesus.png,l: -Hello there !"
        expectOutput = {"type": "dialogue", "name": "Obiwan Kenobi", "image": [
            "truejesus.png", "l"], "text": "Hello there !"}
        result = getDialogue(testTxt)
        self.assertDictEqual(result, expectOutput)

    def test_getBackground(self):
        u"""Test la fonction getBackground, permettant d'indiquer dans 
        le script un changement de background du GUI 
        Le message de base est une ligne type pouvant être mise dans le script 
        Le résultat attendu est un dictionnaire utilisable par l'interpréteur"""

        testTxt = '=space.jpg\n'  # Le retour à la ligne est nécéssaire
        expectOutput = {"type": "bg", "name": "space.jpg"}
        result = getBackground(testTxt)
        self.assertDictEqual(result, expectOutput)

    def test_getDescription(self):
        u"""Test la fonction getDescription, permettant de formatter
        les lignes de texte simple. 
        Le message de base est une ligne type de description pouvant être mise dans le script
        Le résultat attendu est un dictionnaire utilisable par l'interpréteur"""

        testTxt = "I use Arch btw"
        expectOutput = {"type": "description",
                        "name": '', "text": "I use Arch btw"}
        result = getDescription(testTxt)
        self.assertDictEqual(result, expectOutput)

    def test_getHistory(self):
        file = 'test.txt'
        result = getHistory(file)
        expectOutput = [
            {'type': 'inf_sound', 'name': 'duelofthefate.wav'},
            {'type': 'bg', 'name': 'fight.jpg'},
            {'type': 'description', 'name': '', 'text': 'Hello There !\n'},
            {'type': 'sound', 'name': 'lightsaber.wav'},
            {'type': 'dialogue', 'name': 'General Grievous',
             'text': ' "General Kenobi !\n', 'image': ''},
            {'type': 'dialogue', 'name': 'General Grievous',
             'text': ' "General Kenobi ! You\'re a bold one !"', 'image': ''},
            {'type': 'dialogue', 'name': 'Obiwan Kenobi',
             'text': ' "It\'s over Grievous, I\'ve the highgro\n',
             'image': ['obi.png', 'l']},
            {'type': 'stop_inf_sound', 'num': 0},
            {'type': 'choice', 'choice1': ('No', 'dewit.txt'),
             'choice2': ('...', 'tragedy.txt')}]
        self.assertListEqual(result, expectOutput)


if __name__ == "__main__":
    unittest.main()
