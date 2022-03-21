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

ADD_LINE = '+'

BG_START = '='

CHR_IMG = ','

SOUND_START = '♪'  # ALT + 13
INFINITE_SOUND_START = '♫'  # ALT + 14
STOP_SOUND = '/♪'
STOP_INFINITE_SOUND = '/♫'
STOP_ALL_SOUNDS = '§'


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
    if image != '':
        image = image.split(CHR_IMG)

    return {"type": "dialogue", "name": name, "text": text, "image": image}


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


def getSound(line: str) -> dict:
    return {"type": "sound", "name": line[1:-1]}


def getInfiniteSound(line: str) -> dict:
    return {"type": "inf_sound", "name": line[1:-1]}


def stopInfinitesound(line: str) -> dict:
    return {"type": "stop_inf_sound", "num": line[1:-1]}


def stopSound(line: str) -> dict:
    return {"type": "stop_sound", "num": line[1:-1]}


def stopEverySounds() -> dict:
    return {"type": "stop_all"}


def addTextToLastLine(line: str, lastLine: dict) -> dict:
    if 'image' in lastLine:
        image = lastLine["image"]
    else:
        image = ''
    return {"type": "dialogue", "name": lastLine['name'], "text": f'{lastLine["text"][:-1]} {line[1:-1]}', "image": image}


def getHistory(file):
    file_dir = getAbsolutePath.getAbsolutePath(script_dir, DATADIRECTORY+file)
    history = []
    with open(file_dir, encoding='utf-8') as f:
        for line in f.readlines():
            if line[0] == CHOICE_START:
                lineDic = getChoices(line)
            elif line[0] == DIALOGUE_START:
                lineDic = getDialogue(line)
            elif line[0] == BG_START:
                lineDic = getBackground(line)
            elif line[0] == SOUND_START:
                lineDic = getSound(line)
            elif line[0] == ADD_LINE:
                lineDic = addTextToLastLine(line, history[-1])
            elif line[0] == STOP_ALL_SOUNDS:
                lineDic = stopEverySounds()
            elif line[0:2] == STOP_INFINITE_SOUND:
                lineDic = stopInfinitesound(line)
            elif line[0:2] == STOP_SOUND:
                lineDic = stopSound(line)
            else:
                lineDic = getDescription(line)

            history.append(lineDic)
    return history


if __name__ == "__main__":
    file = 'init.txt'
    getHistory(file)
