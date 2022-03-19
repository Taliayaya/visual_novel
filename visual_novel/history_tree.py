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
    R1 = arbre.getRight(True)
    R1.addLeft('LR2', 'LR2.txt')
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
    tree = abr.Arbre('init.txt', 'init.txt' )
    for i in range(0,len(liste)-3, 3):
        print('name',liste[i])
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
    


