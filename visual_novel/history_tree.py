import visual_novel.arbre as abr


def getHistoryTree():
    arbre = abr.Arbre('init', 'init.txt')
    arbre.addLeft('L1', 'L1.txt')
    arbre.addRight('R1', 'R1.txt')
    
    L1 = arbre.getLeft()
    L1.addLeft('LL2', 'LL2.txt')
    L1.addRight('LR2', 'LR2.txt')
    
    LL2 = L1.getLeft()
    LL2.addLeft('LLL3', "LLL3.txt")
    LL2.addRight("LLR3", "LLR3.txt")

    LLL3 = LL2.getLeft()
    LLL3.addLeft("LLLL4", "LLLL4.txt")
    LLL3.addRight("LLLR4", "LLLR4.txt")

    LLR3 = LL2.getRight()
    LLR3.addLeft("LLRL4", "LLRL4.txt")
    LLR3.addRight("LLRR4", "LLRR4.txt")

    LLRL4 = LLR3.getLeft()
    LLRL4.addLeft("LLRLL5", "LLRLL5.txt")
    LLRL4.addRight("LLRLR5", "LLRLR5.txt")

    LR2 = L1.getRight()
    LR2.addLeft("LRL3", "LRL3.txt")
    LR2.addRight("LRR3", "LRR3.txt")

    LRL3 = LR2.getLeft()
    LRL3.addLeft("LRLL4", "LRLL4.txt")
    LRL3.addRight("LRLR4", "LRLR4.txt")

    LRLL4 = LRL3.getLeft()
    LRLL4.addLeft("LRLLL5", "LRLLL5.txt")
    LRLL4.addRight("LRLLR5", "LRLLR5.txt")

    LRLR4 = LRL3.getRight()
    LRLR4.addLeft("LRLRL5", "LRLRL5.txt")
    LRLR4.addRight("LRLRR5", "LRLRR5.txt")

    LRR3 = LR2.getRight()
    LRR3.addLeft("LRRL4", "LRRL4.txt")
    LRR3.addRight("LRRR4", "LRRR4.txt")

    LRRL4 = LRR3.getLeft()
    LRRL4.addLeft("LRRLL5", "LRRLL5.txt")
    LRRL4.addRight("LRRLR5", "LRRLR5.txt")

    LRRLL5 = LRRL4.getLeft()
    LRRLL5.addLeft("LRRLLL6", "LRRLLL6.txt")
    LRRLL5.addRight("LRRLLR6", "LRRLLR6.txt")

    return arbre


if __name__ == "__main__":
    print(
        getHistoryTree())
