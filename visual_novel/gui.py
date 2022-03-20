import string
import sys
import tkinter as tk
from PIL import ImageTk, Image, ImageFilter
import os

from matplotlib.pyplot import grid
import visual_novel.getAbsolutePath
import visual_novel.interpreter as interpreter
import visual_novel.history_tree as htree
import visual_novel.arbre as arbre
import visual_novel.sound as sound
import tkinter.messagebox


# Window
WIDTH = 1000
HEIGHT = 500
# Background Image
IMAGEWIDTH = 1000
IMAGEHEIGHT = 500
BACKGROUND_DIR = 'assets/images/'
MENU_DIR = 'assets/menu/'
# Character Image
CHRIMAGEWIDTH = 100
CHRIMAGEHEIGHT = 300
# Font
FONTSIZE = 12
FONTFAMILY = 'Arial'
# Message Label
LABELWIDTH = 100
script_dir = os.path.dirname(__file__)


class App:
    def __init__(self) -> None:

        self.root = tk.Tk()
        # Modifie les intéractions avec le close icon
        self.root.protocol('WM_DELETE_WINDOW', self.onClosing)
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.resizable(0, 0)
        self.root.title('The Dark Side Of Venice - Visual Novel')
        self.bgimage = "menu.jpg"
        self.chrimage = ('none.png', 'l')
        self.newGame()
        self.soundPlayer = sound.GameSound()
        self.soundPlayer.startInfiniteSound('musique_vive.wav')
        self.root.rowconfigure(2, minsize=30)

    def homePage(self, destroy=False):
        if destroy:
            self.frame.destroy()
            self.soundPlayer.stopEverything()
            return

        # LOAD IMAGES
        self.newGameImg = ImageTk.PhotoImage(Image.open(
            visual_novel.getAbsolutePath.getAbsolutePath(script_dir, f'{MENU_DIR}newGame.jpg')).resize((200, 76)))
        self.continueImg = ImageTk.PhotoImage(Image.open(
            visual_novel.getAbsolutePath.getAbsolutePath(script_dir, f'{MENU_DIR}continue.jpg')).resize((200, 76)))
        self.quitImg = ImageTk.PhotoImage(Image.open(
            visual_novel.getAbsolutePath.getAbsolutePath(script_dir, f'{MENU_DIR}quit.jpg')).resize((200, 76)))

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="none", expand=True)
        play = tk.Button(self.frame, text='Nouvelle Partie',
                         image=self.newGameImg, command=self.startGame, cursor="hand1")
        play.grid(row=0, column=0)
        continueBtn = tk.Button(self.frame, text='Continuer', cursor="hand1",
                                image=self.continueImg, command=self.continueGame)
        continueBtn.grid(row=1, column=0)
        tk.Label(self.frame).grid(row=2, column=0)
        quitBtn = tk.Button(self.frame, text='Quitter',
                            image=self.quitImg, command=self.onClosing)
        quitBtn.grid(row=3, column=0)
        self.soundPlayer.startNewSound('startsound.wav')

    def continueGame(self):
        self.startGame()
        self.loadHistoryFromSave()

    def startGame(self):
        self.homePage(True)
        self.soundPlayer.startNewSound('startsound.wav')
        self.root.bind("<space>", self.setDialogueBox)
        self.menu()
        self.bgimage = 'quai_nuit.png'
        self.setupBackground()
        self.setDialogueBox(False)

    def onClosing(self):
        u"""
        Permet de gérer manuellement l'action de quitter le jeu.

        En quittant le jeu, demande une confirmation et arrête toutes les musiques
        """
        if tkinter.messagebox.askokcancel("Quitter le jeu", "Êtes-vous sûr de vouloir quitter le jeu ? Toute progression non-sauvegardée sera perdue. "):
            self.soundPlayer.stopEverything()
            self.root.quit()
            sys.exit(0)

    def start(self):
        self.setupBackground()
        self.setCharacterMessage('', '', '', False)
        self.homePage()
        # self.root.bind("<space>", self.setDialogueBox)
        # self.menu()
        # self.chooseUsername()
        # self.setDialogueBox(False)
        self.root.mainloop()

    def newGame(self, move=False):
        self.htree = htree.getHistoryTree()
        self.currentFile = self.htree.getFile()
        self.currentLine = 0

        self.changeFile()
        self.isChoosing = False
        self.chrimage = ''
        # self.bgimage = 'quai_nuit.png'
        if move:
            self.setupBackground()
            self.setDialogueBox()

    def changeFile(self):
        self.history = interpreter.getHistory(self.currentFile)

    def nextChapter(self, node: bool):
        u"""
        Change de noeud dans l'histoire et permet d'avancer d'un chapitre

        Précondition:
            node (bool) : correspond si l'histoire continue sur la branche
            gauche (True) ou droite (False) de l'arbre

        Postcondition:
            Réinitialise le compteur de ligne
            Retire la fenêtre de choix
            Récupère le texte du nouveau chapitre
            Affiche le nouveau texte"""
        if node:
            self.htree = self.htree.getLeft()
        else:
            self.htree = self.htree.getRight()
        # Supprime la zone de choix
        self.choiceContainer((None, None), (None, None), True)
        # Récupère le nouveau fichier puis traite l'histoire
        self.currentFile = self.htree.getFile()
        self.changeFile()
        self.currentLine = 0
        # Permet à l'utilisateur de continuer l'histoire
        self.isChoosing = False
        self.setDialogueBox(True)

    def loadHistoryFromSave(self):
        u"""Permet de charger la dernière sauvegarde effectuée
        Le fichier de sauvegarde est interprété, transformé en un
        arbre d'histoire, navigué dedans puis met à jour l'affichage
        graphique."""
        mainTree = htree.getHistoryTree()
        save = arbre.loadSave()
        self.htree = arbre.saveToTree(mainTree, save)
        self.currentLine = 0
        self.currentFile = self.htree.getFile()
        self.changeFile()
        self.isChoosing = False
        self.setDialogueBox()

    def setDialogueBox(self, destroy=True):
        u"""
        Traite l'histoire du jeu et décide quel affichage
        chaque ligne doit recevoir en fonction de son type.

        Récupère la variable self.history et la ligne actuelle
        pour récupérer un dictionnaire. Ce dictionnaire contient
        une clef `type` qui identifie chaque ligne.

        Précondition:
            destroy : bool
                indique si la frame précédente doit être
                détruite ou non. True pour destroy, False pour keep.
                True par défaut.

        Postcondition:
            Renvoie vers l'une des fonctions permettant de traiter
            le cas de la ligne actuelle.
            Augmente de 1 la ligne actuelle dans l'histoire.
        """

        # Si l'utilisateur est dans un choix, empêche le refresh de
        # la boite de dialogue pour éviter d'en créer plus d'une
        if self.isChoosing:
            return

        line = self.history[self.currentLine]

        if line['type'] == 'bg':
            self.bgimage = line['name']
            self.setupBackground()
            self.currentLine += 1
            return self.setDialogueBox(False)

        elif line["type"] == "sound":
            self.soundPlayer.startNewSound(line['name'])
            self.currentLine += 1
            return self.setDialogueBox(False)

        elif line["type"] == "inf_sound":
            self.soundPlayer.startInfiniteSound(line["name"])
            self.currentLine += 1
            return self.setDialogueBox(False)
        elif line["type"] == 'stop_inf_sound':
            self.soundPlayer.stopInfiniteSound(line['num'])
            self.currentLine += 1
            return self.setDialogueBox(False)
        elif line['type'] == 'stop_sound':
            self.soundPlayer.stopSound(line["num"])
            self.currentLine += 1
            return self.setDialogueBox(False)
        elif line['type'] == 'stop_all':
            self.soundPlayer.stopEverything()
            self.currentLine += 1
            return self.setDialogueBox(False)
        print(line)

       # Renvoie vers l'affichage d'un texte

        if line['type'] != "choice" and line['type'] != 'bg':

            if 'image' in line:
                self.setCharacterMessage(
                    line["name"], line['text'], line['image'], destroy)
            else:
                self.setCharacterMessage(
                    line["name"], line['text'], '', destroy)
        else:
            # Renvoie vers une zone de choix
            choice1 = line["choice1"]
            choice2 = line["choice2"]
            self.choiceContainer(choice1, choice2)
            self.isChoosing = True
        # Augmente d'une ligne tant que l'historie n'est pas finie
        if self.currentLine+1 < len(self.history):
            self.currentLine += 1

    def chooseUsername(self):
        u"""
        Affiche un input permettant à l'utilisateur
        de choisir son username au début du jeu.

        Postcondition:
            Affiche l'input indiquant à l'utilisateur
            de choisir son nom et un bouton permettant
            de valider l'input puis commencer le jeu.
        """
        label = tk.Label(self.root, text="Choisi ton nom : ")
        value = tk.StringVar()
        input = tk.Entry(self.root, textvariable=string, width=50)
        input.grid(row=3, column=0)
        bouton = tk.Button(self.root, text="Commencer l'aventure",
                           command=lambda: self.setCharacterMessage(input.get(), 'No one can choose who he is in this world'))
        bouton.pack()

    def menu(self):
        u"""
        Permet la création du menu supérieur

        Postcondition:
            Crée le menu qui contient les catégories:
            - FICHIER
                - Nouvelle Partie
                - Sauvegarder
                - Charger une sauvegarde
                - Quitter
            - EDITER
            - AIDE
        """
        self.menuContainer = tk.Menu(self.root)

        # FICHIER MENU
        self.fichier = tk.Menu(self.menuContainer, tearoff=0)
        self.fichier.add_command(
            label="Nouvelle Partie", command=lambda: self.newGame(True))
        self.fichier.add_command(
            label="Sauvegarder", command=lambda: arbre.writeSave(self.htree))
        self.fichier.add_command(
            label="Charger une sauvegarde", command=self.loadHistoryFromSave)
        self.fichier.add_separator()
        self.fichier.add_command(label="Quitter", command=self.onClosing)
        self.menuContainer.add_cascade(label="Fichier", menu=self.fichier)

        # EDIT MENU
        self.edit = tk.Menu(self.menuContainer, tearoff=0)
        self.menuContainer.add_cascade(label="Éditer", menu=self.edit)

        # HELP MENU
        self.help = tk.Menu(self.menuContainer, tearoff=0)
        self.menuContainer.add_cascade(label="Aide", menu=self.help)

        self.root.config(menu=self.menuContainer)

    def setupBackground(self, changeBg=True):
        u"""
        Permet de gérer l'affichage du background et des images
        des personnages.

        Préconditions:
            changeBg : bool
                Indique s'il faut change le background ou bien
                l'image de personnage

        Affiche l'image choisie comme décors du jeu
        Postcondition:
            Change le type d'image demandé
        """

        if changeBg:
            self.canv = tk.Canvas(self.root, width=IMAGEWIDTH,
                                  height=IMAGEHEIGHT)
            img = visual_novel.getAbsolutePath.getAbsolutePath(
                script_dir, f'{BACKGROUND_DIR}bg/{self.bgimage}')
            self.bg = ImageTk.PhotoImage(Image.open(
                img).resize((IMAGEWIDTH, IMAGEHEIGHT), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(1)))
            self.canv.create_image(0, 0, anchor=tk.NW, image=self.bg)
        else:
            if self.chrimage:
                chrimg = visual_novel.getAbsolutePath.getAbsolutePath(
                    script_dir, f'{BACKGROUND_DIR}chr/{self.chrimage[0]}')
                self.canv.place(x=0, y=0)
                self.chrbg = ImageTk.PhotoImage(Image.open(
                    chrimg).resize((200, 400), Image.ANTIALIAS))
                # left : 10, 120
                if self.chrimage[1] == 'r':
                    self.canv.create_image(
                        810, 120, anchor=tk.NW, image=self.chrbg)
                else:
                    self.canv.create_image(
                        10, 120, anchor=tk.NW, image=self.chrbg)

    def choiceContainer(self, choice1: tuple, choice2: tuple, destroy=False):
        u"""
        Affiche deux boutons permettant de passer dans une
        nouvelle branche de l'arbre. Demande au joueur de faire un choix

        Préconditions:
            choice1 : tuple
                contient le message du bouton1
                et son fichier de destination
            choice2 : tuple
                contient le message du bouton2
                et son fichier de destination

        Postcondition:
            Affiche deux boutons de message tuple[0]
            et de destination tuple[1]
        """
        if destroy:
            self.choiceFrame.destroy()
            return
        self.choiceFrame = tk.Frame(
            self.root, relief=tk.GROOVE)
        self.choiceFrame.pack(fill="none", expand=True)

        self.buttonLeft = tk.Button(
            self.choiceFrame, text=choice1[0], padx=10, pady=10, command=lambda: self.nextChapter(True))
        self.buttonRight = tk.Button(
            self.choiceFrame, text=choice2[0], padx=10, pady=10, command=lambda: self.nextChapter(False))

        self.buttonLeft.pack(expand="yes")
        self.buttonRight.pack(expand="yes")
        print(self.choiceFrame)

    def setCharacterMessage(self, name: str, message: str, image: str, destroy: bool = True):
        u"""
        Affiche le message du personnage sur l'interface
        et retire le précédent

        Préconditions:
            name : str
                est le nom du personnage qui parle
            message : str
                est le message associé au personnage
            destroy : bool
                retire ou non le message précédent

        Postcondition:
            Affiche le message name/message sur l'interface
        """

        if destroy:
            self.char.destroy()
        self.char = tk.LabelFrame(self.root, text=name, padx=20, pady=20)
        self.char.pack(side=tk.BOTTOM, padx=10, pady=10)
        if message:
            self.message = tk.Label(self.char, text=message, wraplength=900, justify=tk.CENTER,
                                    width=LABELWIDTH, font=(FONTFAMILY, FONTSIZE))
            self.message.pack()
        if image:
            self.chrimage = image
        else:
            self.chrimage = ('none.png', 'l')
        self.setupBackground(False)


if __name__ == "__main__":
    app = App()
    app.start()
