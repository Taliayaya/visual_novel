import visual_novel.arbre as abr


def getHistoryTree():
    arbre = abr.Arbre('init', 'init.txt')
    arbre.addLeft('L1', 'L1.txt')
    arbre.addRight('R1', 'R1.txt')
    L1 = arbre.getLeft()
    L1.addLeft('LL2', 'LL2.txt')
    R1 = arbre.getRight()
    R1.addLeft('LR2', 'LR2.txt')
    return arbre


if __name__ == "__main__":
    print(
        getHistoryTree())
