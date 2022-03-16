import visual_novel.getAbsolutePath as getAbsolutePath
import tkinter.messagebox
import os

script_dir = os.path.dirname(__file__)
SAVEDIRECTORY = 'assets/saves/'


class Arbre:
    u"""
    Représente un Arbre Binaire

    Contient des noeuds qui contiennent eux-même
    0, 1 ou 2 autres noeuds : un fils gauche et un fils droit 
    L'initialisation de la class Arbre crée un noeud racine. 
    Il est possible de modifier, d'ajouter ou d'accéder aux
    autres noeuds en utilisant les méthodes de la class Arbre.

    Attributs: 
    ----------
        value : str 
            La valeur associée au noeud de l'arbre
        file : str 
            Le nom du fichier associé au noeud de l'arbre
        left : Arbre | None
            Le fils gauche du noeud. Peut contenir un autre noeud
            de la class Arbre ou None par défaut
        right : Arbre | None
            Le fils droit du noeud. Peut contenir un autre noeud
            de la class Arbre ou None par défaut

    Méthodes:
    ---------
    getValue()
        Renvoie l'attribut value du noeud actuel de l'instance de Arbre
    getFile()
        Renvoie l'attribut file du noeud actuel de l'instance de Arbre
    getLeft()
        Renvoie le fils gauche du noeud actuel 
    getRight()
        Renvoie le fils droti du noeud actuel
    addLeft(value: str, file: str)
        Change le fils gauche du noeud actuel en un nouveau noeud  
        ayant comme attributs value et file
    addRight(value: str, file: str)
        Change le fils droit du noeud actuel en un nouveau noeud 
        ayant comme attributs value et file
    """
    choices = []

    def __init__(self, value: str, file: str, left=None, right=None) -> None:
        u"""
        Initialise le noeud racine de l'arbre binaire ou un de
        ses noeuds.

        Préconditions:
            value :  str
                correspond à la valeur détenue par le noeud.
            file : str
                est le nom du fichier associé au noeud. 
            left : Arbre | None
                est le fils gauche du noeud. Peut contenir
                un sous noeud ou None par défaut.
            right : Arbre | None 
                est le fils droit du noeud. Peut contenir 
                un sous noeud ou None par défaut. 

        Postconditions: 
            Initialise une instance de la class Arbre 
            en créant un noeud à l'aide des arguments donnés 
        """
        self._value = value
        self._left = left
        self._right = right
        self._file = file

    def __str__(self) -> str:
        u"""
        Affiche l'arbre binaire à partir du noeud actuel. 

        Postcondition: 
            Affiche la valeur et le fichier du noeud actuel de
            l'arbre binaire ainsi que son fils gauche et son fils droit. 
            valeur[fichier](fils gauche)(fils droit)
        """
        return f'{self._value}[{self._file}]({self._left}, {self._right})'

    def getValue(self) -> str:
        u"""
        Renvoie la valeur associée au noeud actuel 
        """
        return self._value

    def getFile(self) -> str:
        u"""
        Renvoie le nom du fichier associé au noeud actuel
        """
        return self._file

    def getLeft(self) -> 'Arbre':
        u"""
        Renvoie le fils gauche du noeud actuel

        Postcondition: 
            Renvoie le fis gauche du noeud actuel. 
            Cela peut être un autre noeud de la class Arbre 
            ou None si le noeud actuel ne possède pas de fils
            gauche. 
        """
        self.choices.append('L')
        return self._left

    def getRight(self) -> 'Arbre':
        u"""
        Renvoie le fils droit du noeud actuel

        Postcondition: 
            Renvoie le fis droit du noeud actuel. 
            Cela peut être un autre noeud de la class Arbre 
            ou None si le noeud actuel ne possède pas de fils
            droit. 
        """
        self.choices.append('R')
        return self._right

    def addLeft(self, value: str, file: str) -> None:
        u"""
        Ajoute un fils gauche au noeud actuel

        Cela ajoute un fils gauche à partir du noeud actuel et non 
        pas en bas de l'Arbre. Si le noeud actuel possède déjà un fils
        gauche, son contenu et ses enfants seront supprimés et remplacés
        par le nouveau noeud. 

        Préconditions: 
            value : str
                est la valeur qui sera associée au fils gauche 
                du noeud actuel. 
            file : str 
                est le nom du fichier qui sera associé au fils
                gauche du noeud actuel. 

        Postcondition: 
            Change le fils gauche du noeud actuel en un 
            nouveau sous-noeud à partir des arguments données.
        """
        self._left = Arbre(value, file)

    def addRight(self, value: str, file: str) -> None:
        u"""
        Ajoute un fils droit au noeud actuel

        Cela ajoute un fils droit à partir du noeud actuel et non 
        pas en bas de l'Arbre. Si le noeud actuel possède déjà un fils
        droit, son contenu et ses enfants seront supprimés et remplacés
        par le nouveau noeud. 

        Préconditions: 
            value : str
                est la valeur qui sera associée au fils droit 
                du noeud actuel. 
            file : str 
                est le nom du fichier qui sera associé au fils
                droit du noeud actuel. 

        Postcondition: 
            Change le fils droit du noeud actuel en un 
            nouveau sous-noeud à partir des arguments données.
        """
        self._right = Arbre(value, file)


def writeSave(abr):
    choices = ' '.join(abr.choices)
    filelocation = getAbsolutePath.getAbsolutePath(
        script_dir, f'{SAVEDIRECTORY}save.txt')
    try:
        with open(filelocation, 'w') as f:
            f.write(choices)
        tkinter.messagebox.showinfo(
            "Sauvegarde réussie",  "La partie a été sauvergardée !")
    except Exception:
        tkinter.messagebox.showerror(
            "Échec de la sauvegarde", "La sauvegarde de la partie a échoué. Veuillez réessayer.")


if __name__ == "__main__":
    abr = Arbre('Init', 'init.txt')
    abr.addLeft('L1', 'l1.txt')
    abr = abr.getLeft()
    abr.addRight('R2', '')
    abr = abr.getRight()
    print(abr.choices)
    writeSave(abr)
