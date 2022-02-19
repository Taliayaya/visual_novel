class Arbre:
    def __init__(self, value, left=None, right=None) -> None:
        self._value = value  # Oui|Non%
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f'{self._value}({self._left}, {self._right})'

    def getValue(self):
        return self._value

    def getLeft(self):
        return self._left

    def getRight(self):
        return self._right

    def addLeft(self, value):
        self._left = value

    def addRight(self, value):
        self._right = value


def addNewNode(A, value):
    if A.getValue() == value:
        return False
    elif A.getValue() > value:
        if A.getLeft() is None:
            A.addLeft(value)
            return True
        return addNewNode(A.getLeft(), value)
    else:
        if A.getRight() is None:
            A.addRight(value)
            return True
        return addNewNode(A.getRight(), value)


if __name__ == "__main__":
    abr = Arbre(5)
    print(abr)
