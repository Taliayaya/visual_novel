import string
import tkinter as tk
from PIL import ImageTk, Image
import os
import getAbsolutePath

# Background Image
IMAGEWIDTH = 1000
IMAGEHEIGHT = 400

script_dir = os.path.dirname(__file__)


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()

    def start(self):
        self.setupBackground()
        self.menu()
        self.choiceContainer('Yes', 'No')
        self.setCharacterMessage('Ilan', 'Hey, you\'re finally awake !')
        self.chooseUsername()
        self.root.mainloop()

    def chooseUsername(self):
        label = tk.Label(self.root, text="Choisi ton nom : ")
        value = tk.StringVar()
        input = tk.Entry(self.root, textvariable=string, width=50)
        input.grid(row=3, column=0)
        bouton = tk.Button(self.root, text="Commencer l'aventure",
                           command=lambda: self.setCharacterMessage(input.get(), 'No one can choose who he is in this world'))
        bouton.grid(row=4, column=0)

    def menu(self):
        """Create the upper menu
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
        img = getAbsolutePath.getAbsolutePath(
            script_dir, '../assets/images/space.jpg')
        self.bg = ImageTk.PhotoImage(Image.open(
            img).resize((IMAGEWIDTH, IMAGEHEIGHT), Image.ANTIALIAS))
        canv = tk.Canvas(self.root, width=IMAGEWIDTH,
                         height=IMAGEHEIGHT, bg="white")
        canv.grid(row=0, column=0)
        canv.create_image(0, 0, anchor=tk.NW, image=self.bg)

    def choiceContainer(self, choice1, choice2):
        self.choiceFrame = tk.Frame(
            self.root, relief=tk.GROOVE, padx=10, pady=10)
        self.choiceFrame.grid(row=1, column=0)

        self.buttonLeft = tk.Button(
            self.choiceFrame, text=choice1, padx=10, pady=10)
        self.buttonRight = tk.Button(
            self.choiceFrame, text=choice2, padx=10, pady=10)

        self.buttonLeft.pack(side=tk.LEFT, expand="yes", padx=5, pady=5)
        self.buttonRight.pack(side=tk.RIGHT, expand="yes", padx=5, pady=5)

    def setCharacterMessage(self, name, message):
        self.char = tk.LabelFrame(self.root, text=name, padx=20, pady=20)
        self.char.grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.char, text=message).pack()


if __name__ == "__main__":
    app = App()
    app.start()
