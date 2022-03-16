import visual_novel.getAbsolutePath as getAbsolutePath
import os

script_dir = os.path.dirname(__file__)
DATADIRECTORY = 'assets/history/'

# SYMBOLES :
CHOICE_START = '#'
CHOICE_DELIMITER = '|'
CHOICE_DESTINATION = '~'

DIALOGUE_START = '-'
DIALOGUE_DELIMITER = ': -'
DIALOGUE_CHR_IMAGE = '@'

BG_START = '='


def getChoices(line: str) -> list:
    u"""Récupère dans la ligne la question et forme une liste contenant les questions et leur destination

    Précondition:
        line (str) est la ligne où une zone de choix a été détectée

    Postcondition:
        Renvoie une liste contenant des tuples de la forme (choix, destination)

    Exemple:
        >>> foo = '#No~dewit.txt|...~tragedy.txt$'
        >>> getChoices(foo)
        >>> # Expected Output
        >>> [('No', 'dewit.txt'), ('...', 'tragedy.txt')]
        """
    choices = line[1: -1]
    choice1, choice2 = choices.split(CHOICE_DELIMITER)
    choice1, choice1_dest = choice1.split(CHOICE_DESTINATION)
    choice2, choice2_dest = choice2.split(CHOICE_DESTINATION)
    return {"type": "choice", "choice1": (choice1, choice1_dest), "choice2": (choice2, choice2_dest)}


def getDialogue(line: str) -> dict:
    u"""Récupère une ligne de dialogue et la formate pour l'utilisation

    Dans la ligne donnée, extrait le personnage qui parle et son texte et le
    stock dans un dictionnaire
    La séparation entre le personnage et son texte est repéré par `: -`
    Le dialogue est repéré par un hyphen au début de la ligne (`-`)

    Précondition:
        line (str): est la ligne à extraire

    Postcondition:
        Renvoie un dictionnaire contenant le nom du personnage, son dialogue et
        le type extrait (ici dialogue)

    Exemple:
        >>> foo = "-Palpatine : - Do you know the Tragedy of Darth Plagueis the Wise ?"
        >>> getDialogue(foo)
        Expected Output :
        >>> {"type":"Dialogue", "name":"Palpatine", "text":"Do you know the Tragedy of Darth Plageuis the Wise ?"}
    """
    name, text = line.split(DIALOGUE_DELIMITER)
    name, image = name[1:].split(DIALOGUE_CHR_IMAGE)
    return {"type": "dialogue", "name": name, "text": text, "image":image}

def getBackground(line: str) -> dict:
    u""""""
    return {"type": "bg", "name": line[1:-1]}

def getDescription(line: str) -> dict:
    u"""Récupère une ligne de description et la formate pour l'utilisation

    Une ligne de description est répérée si elle ne comporte ni Dialogue, ni Choix.

    Précondition:
        line (str): est la ligne à extraire

    Postcondition:
        Renvoie un dictionnaire contenant un nom vide, signifiant une description, la description et
        le type extrait (ici une descriptipn)

    Exemple:
        >>> foo = "You're finally awake !"
        >>> getDescription(foo)
        Expected Output :
        >>> {"type":"description", "name":"", "text":'"You\'re finally awake !"'}
    """
    return {"type": "description", "name": "", "text": line}


def getHistory(file):
    file_dir = getAbsolutePath.getAbsolutePath(script_dir, DATADIRECTORY+file)
    history = []
    with open(file_dir, encoding='utf-8') as f:
        for line in f.readlines():
            if line[0] == CHOICE_START:
                history.append(getChoices(line))
            elif line[0] == DIALOGUE_START:
                history.append(getDialogue(line))
            elif line[0] == BG_START:
                history.append(getBackground(line))
            else:
                history.append(getDescription(line))
    return history


if __name__ == "__main__":
    file = 'init.txt'
    print(getHistory(file))
