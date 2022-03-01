import string
import tkinter as tk
from PIL import ImageTk, Image
import os
import visual_novel.getAbsolutePath
import visual_novel.interpreter as interpreter

# Background Image
IMAGEWIDTH = 1000
IMAGEHEIGHT = 400

script_dir = os.path.dirname(__file__)


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.currentFile = 'init.txt'
        self.currentLine = 0
        self.changeFile()

    def start(self):
        self.root.bind("<space>", lambda x: self.setDialogueBox())
        self.setupBackground()
        self.menu()
        self.choiceContainer('Yes', 'No')
        self.chooseUsername()
        self.setDialogueBox(False)
        self.root.mainloop()

    def changeFile(self):
        self.history = interpreter.getHistory(self.currentFile)

    def setDialogueBox(self, destroy=True):
        self.setCharacterMessage(
            "Ilan", self.history[self.currentLine], destroy)
        if self.currentLine+1 < len(self.history):
            self.currentLine += 1

    def chooseUsername(self):
        label = tk.Label(self.root, text="Choisi ton nom : ")
        value = tk.StringVar()
        input = tk.Entry(self.root, textvariable=string, width=50)
        input.grid(row=3, column=0)
        bouton = tk.Button(self.root, text="Commencer l'aventure",
                           command=lambda: self.setCharacterMessage(input.get(), 'No one can choose who he is in this world'))
        bouton.grid(row=4, column=0)

    def menu(self):
        """
        Permet la création du menu

        Contient les catégories:
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
        """
        Affiche l'image choisie comme décors du jeu
        """
        img = visual_novel.getAbsolutePath.getAbsolutePath(
            script_dir, 'assets/images/space.jpg')
        self.bg = ImageTk.PhotoImage(Image.open(
            img).resize((IMAGEWIDTH, IMAGEHEIGHT), Image.ANTIALIAS))
        canv = tk.Canvas(self.root, width=IMAGEWIDTH,
                         height=IMAGEHEIGHT, bg="white")
        canv.grid(row=0, column=0)
        canv.create_image(0, 0, anchor=tk.NW, image=self.bg)

    def choiceContainer(self, choice1: tuple, choice2: tuple):
        """
        Affiche deux boutons permettant de passer dans une
        nouvelle branche de l'arbre. Demande au joueur de faire un choix

        Préconditions:
            - choice1 (tuple): contient le message du bouton1 et son fichier de destination
            - choice2 (tuple): contient le message du bouton2 et son fichier de destination

        Postcondition:
            Affiche deux boutons de message tuple[0] et de destination tuple[1]
        """
        self.choiceFrame = tk.Frame(
            self.root, relief=tk.GROOVE, padx=10, pady=10)
        self.choiceFrame.grid(row=1, column=0)

        self.buttonLeft = tk.Button(
            self.choiceFrame, text=choice1, padx=10, pady=10)
        self.buttonRight = tk.Button(
            self.choiceFrame, text=choice2, padx=10, pady=10)

        self.buttonLeft.pack(side=tk.LEFT, expand="yes", padx=5, pady=5)
        self.buttonRight.pack(side=tk.RIGHT, expand="yes", padx=5, pady=5)

    def setCharacterMessage(self, name: str, message: str, destroy: bool=True):
        """Affiche le message du personnage sur l'interface et retire le précédent

        Préconditions:
            - name (str) est le nom du personnage qui parle
            - message (str) est le message associé au personnage
            - destroy (bool) retire ou non le message précédent

        Postcondition:
            Affiche le message name/message sur l'interface"""
        if destroy:
            self.char.destroy()
        self.char = tk.LabelFrame(self.root, text=name, padx=20, pady=20)
        self.char.grid(row=2, column=0, padx=10, pady=10)
        self.message = tk.Label(self.char, text=message)
        self.message.grid(row=0, column=0)


if __name__ == "__main__":
    app = App()
    app.start()
