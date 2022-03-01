class Arbre:
    def __init__(self, value, file: str, left=None, right=None) -> None:
        self._value = value  # Oui|Non%
        self._left = left
        self._right = right
        self._file = file

    def __str__(self) -> str:
        return f'{self._value}[{self._file}]({self._left}, {self._right})'

    def getValue(self):
        return self._value

    def getFile(self):
        return self._file

    def getLeft(self):
        return self._left

    def getRight(self):
        return self._right

    def addLeft(self, value, file):
        self._left = Arbre(value, file)

    def addRight(self, value, file):
        self._right = Arbre(value, file)


if __name__ == "__main__":
    abr = Arbre('Init', 'init.txt')
    print(abr)
