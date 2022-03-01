import visual_novel.getAbsolutePath as getAbsolutePath
import os

script_dir = os.path.dirname(__file__)
DATADIRECTORY = 'assets/history/'

# SYMBOLES :
CHOICE_START = '#'
CHOICE_DELIMITER = '|'
CHOICE_DESTINATION = '~'


def getChoices(line: str) -> list:
    """Récupère dans la ligne la question et forme une liste contenant les questions et leur destination

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
    return [(choice1, choice1_dest), (choice2, choice2_dest)]


def getHistory(file):
    file_dir = getAbsolutePath.getAbsolutePath(script_dir, DATADIRECTORY+file)
    history = []
    with open(file_dir) as f:
        for line in f.readlines():
            if line[0] == CHOICE_START:
                history.append(getChoices(line))
            else:
                history.append(line)
    return history


if __name__ == "__main__":
    file = 'init.txt'
    print(getHistory(file))
