import string
import tkinter as tk
from PIL import ImageTk, Image
import os
import visual_novel.getAbsolutePath
import visual_novel.interpreter as interpreter
import visual_novel.history_tree as htree

# Background Image
IMAGEWIDTH = 1000
IMAGEHEIGHT = 400
BACKGROUND_DIR = 'assets/images/'

script_dir = os.path.dirname(__file__)


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.htree = htree.getHistoryTree()
        self.currentFile = self.htree.getFile()
        self.currentLine = 0
        self.changeFile()
        self.isChoosing = False

    def start(self):
        self.root.bind("<space>", lambda x: self.setDialogueBox())
        self.setupBackground()
        self.menu()
        self.chooseUsername()
        self.setDialogueBox(False)
        self.root.mainloop()

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
        self.choiceContainer((None, None), (None,None), True)
        # Récupère le nouveau fichier puis traite l'histoire
        self.currentFile = self.htree.getFile()
        self.changeFile()
        self.currentLine = 0
        # Permet à l'utilisateur de continuer l'histoire
        self.isChoosing = False
        self.setDialogueBox(True)

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
        # Renvoie vers l'affichage d'un texte
        if self.history[self.currentLine]['type'] != "choice":
            self.setCharacterMessage(
           self.history[self.currentLine]["name"], self.history[self.currentLine]["text"], destroy)
        else:
            # Renvoie vers une zone de choix
            choice1 = self.history[self.currentLine]["choice1"]
            choice2 = self.history[self.currentLine]["choice2"]
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
        bouton.grid(row=4, column=0)

    def menu(self):
        u"""
        Permet la création du menu supérieur

        Postcondition:
            Crée le menu qui contient les catégories:
            - FICHIER
                - Nouvelle Partie
                - Sauvegarder
                - Quitter
            - EDITER
            - AIDE
        """
        self.menuContainer = tk.Menu(self.root)

        # FICHIER MENU
        self.fichier = tk.Menu(self.menuContainer, tearoff=0)
        self.fichier.add_command(label="Nouvelle Partie")
        self.fichier.add_command(label="Sauvegarder")
        self.fichier.add_separator()
        self.fichier.add_command(label="Quitter", command=self.root.quit)
        self.menuContainer.add_cascade(label="Fichier", menu=self.fichier)

        # EDIT MENU
        self.edit = tk.Menu(self.menuContainer, tearoff=0)
        self.menuContainer.add_cascade(label="Éditer", menu=self.edit)

        # HELP MENU
        self.help = tk.Menu(self.menuContainer, tearoff=0)
        self.menuContainer.add_cascade(label="Aide", menu=self.help)

        self.root.config(menu=self.menuContainer)

    def setupBackground(self):
        u"""
        Affiche l'image choisie comme décors du jeu
        """
        img = visual_novel.getAbsolutePath.getAbsolutePath(
            script_dir, f'{BACKGROUND_DIR}space.jpg')
        self.bg = ImageTk.PhotoImage(Image.open(
            img).resize((IMAGEWIDTH, IMAGEHEIGHT), Image.ANTIALIAS))
        canv = tk.Canvas(self.root, width=IMAGEWIDTH,
                         height=IMAGEHEIGHT, bg="white")
        canv.grid(row=0, column=0)
        canv.create_image(0, 0, anchor=tk.NW, image=self.bg)

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
            self.root, relief=tk.GROOVE, padx=10, pady=10)
        self.choiceFrame.grid(row=1, column=0)

        self.buttonLeft = tk.Button(
            self.choiceFrame, text=choice1[0], padx=10, pady=10, command=lambda: self.nextChapter(True))
        self.buttonRight = tk.Button(
            self.choiceFrame, text=choice2[0], padx=10, pady=10, command=lambda: self.nextChapter(False))

        self.buttonLeft.pack(side=tk.LEFT, expand="yes", padx=5, pady=5)
        self.buttonRight.pack(side=tk.RIGHT, expand="yes", padx=5, pady=5)
        print(self.choiceFrame)

    def setCharacterMessage(self, name: str, message: str, destroy: bool=True):
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
        self.char.grid(row=2, column=0, padx=10, pady=10)
        self.message = tk.Label(self.char, text=message)
        self.message.grid(row=0, column=0)


if __name__ == "__main__":
    app = App()
    app.start()
