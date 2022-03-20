import visual_novel.arbre as abr
import visual_novel.getAbsolutePath as gap
import json
import os

script_dir = os.path.dirname(__file__)


def getHistoryTree():
    arbre = abr.Arbre('init', 'init.txt')
    arbre.addLeft('L1', 'L1.txt')
    arbre.addRight('R1', 'R1.txt')

    L1 = arbre.getLeft(True)
    L1.addLeft('LL2', 'LL2.txt')
    L1.addRight('LR2', 'LR2.txt')

    LL2 = L1.getLeft(True)
    LL2.addLeft('LLL3', "LLL3.txt")
    LL2.addRight("LLR3", "LLR3.txt")

    LLL3 = LL2.getLeft(True)
    LLL3.addLeft("LLLL4", "LLLL4.txt")
    LLL3.addRight("LLLR4", "LLLR4.txt")

    LLR3 = LL2.getRight(True)
    LLR3.addLeft("LLRL4", "LLRL4.txt")
    LLR3.addRight("LLRR4", "LLRR4.txt")

    LLRL4 = LLR3.getLeft(True)
    LLRL4.addLeft("LLRLL5", "LLRLL5.txt")
    LLRL4.addRight("LLRLR5", "LLRLR5.txt")

    LR2 = L1.getRight(True)
    LR2.addLeft("LRL3", "LRL3.txt")
    LR2.addRight("LRR3", "LRR3.txt")

    LRL3 = LR2.getLeft(True)
    LRL3.addLeft("LRLL4", "LRLL4.txt")
    LRL3.addRight("LRLR4", "LRLR4.txt")

    LRLL4 = LRL3.getLeft(True)
    LRLL4.addLeft("LRLLL5", "LRLLL5.txt")
    LRLL4.addRight("LRLLR5", "LRLLR5.txt")

    LRLR4 = LRL3.getRight(True)
    LRLR4.addLeft("LRLRL5", "LRLRL5.txt")
    LRLR4.addRight("LRLRR5", "LRLRR5.txt")

    LRR3 = LR2.getRight(True)
    LRR3.addLeft("LRRL4", "LRRL4.txt")
    LRR3.addRight("LRRR4", "LRRR4.txt")

    LRRL4 = LRR3.getLeft(True)
    LRRL4.addLeft("LRRLL5", "LRRLL5.txt")
    LRRL4.addRight("LRRLR5", "LRRLR5.txt")

    LRRLL5 = LRRL4.getLeft(True)
    LRRLL5.addLeft("LRRLLL6", "LRRLLL6.txt")
    LRRLL5.addRight("LRRLLR6", "LRRLLR6.txt")

    return arbre


def getJson():
    filelocation = gap.getAbsolutePath(script_dir, 'assets/history/story.json')
    with open(filelocation, 'r') as f:
        data = json.load(f)['root']
    return data


def jsonToList(json, parent=None):
    global liste
    if 'left' in json and 'file' in json:
        left = jsonToList(json['left'], parent)
        liste.append(left)
    if 'right' in json and 'file' in json:
        right = jsonToList(json['right'], parent)
        liste.append(right)
    return json['file'] if 'file' in json else None


def listToTree(liste):
    tree = abr.Arbre('init.txt', 'init.txt')
    for i in range(0, len(liste)-3, 3):
        print('name', liste[i])
        print('left', liste[i+1])
        print('right', liste[i+2])


if __name__ == "__main__":
    print(
        getHistoryTree())
    data = getJson()
    liste = []
    print(jsonToList(data))
    print(liste)
    liste = liste[::-1]
    print(liste)
