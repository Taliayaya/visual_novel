import visual_novel.arbre as abr

def getHistoryTree():
    arbre = abr.Arbre('init', 'init.txt')
    arbre.addLeft('L1', 'L1.txt')
    arbre.addRight('R1', 'R1.txt')
    print(arbre)
    return arbre
if __name__ == "__main__":
    getHistoryTree()
