import visual_novel.getAbsolutePath
import os
import multiprocessing
import playsound as ps

SOUND_DIR = 'assets/audio/'
script_dir = os.path.dirname(__file__)


class GameSound:
    """Permet de gérer les sons du jeu"""

    def __init__(self) -> None:
        self._music_playing = []
        self._infinite_music_playing = []

    def _infiniteSound(self, soundName: str) -> '_infiniteSound':
        u"""
        Joue un son à l'infini jusqu'à la fin du programme

        Précondition: 
            soundName : str
                Le nom du son à jouer à l'infini

        Postcondition:
            Lance la fonction startNewSound en boucle sans jamais s'arrêter
            dès que le son est terminé
        """
        soundThread = multiprocessing.Process(
            target=self.startNewSound, args=(soundName,))
        soundThread.start()
        soundThread.join()
        print(self._music_playing)
        return self._infiniteSound(soundName)

    def startInfiniteSound(self, soundName: str):
        u"""
        Lance un son pour le jouer à l'infini mais pouvant être
        arrêté pendant l'exécution du programme

        Précondition:
            soundName : str
                Le nom du son à jouer à l'infini

        Postcondition: 
            Joue le son en boucle : 
            Lance la fonction _infiniteSound dans un thread et
            l'ajoute dans la liste des sons qui jouent à l'infini.

        """
        infiniteThread = multiprocessing.Process(
            target=self._infiniteSound, args=(soundName,))
        self._infinite_music_playing.append(infiniteThread)
        infiniteThread.start()

    def startNewSound(self, soundName: str):
        u"""
        Permet d'ajouter une nouvelle musique

        Précondition:
            soundName : str
                correspond au nom du fichier audio à jouer (avec son extension)

        Postcondition:
            Ajoute le son à la liste des sons lancés et joue l'audio
        """
        # Charge le fichier
        soundFile = visual_novel.getAbsolutePath.getAbsolutePath(
            script_dir, f'{SOUND_DIR}{soundName}')
        # Crée un thread pour lancer en simultané une musique
        soundThread = multiprocessing.Process(
            target=ps.playsound, args=(soundFile,))

        # Ajoute à la liste des threads de musiques en train de jouer
        self._music_playing.append(soundThread)

        # Lance la musique
        soundThread.start()

    def stopSound(self, num: int):
        u"""
        Met fin au thread associé au son au numéro donné

        Précondition:
            num : int
                la position du thread dans la liste des sons

        Postcondition:
            Arrête le son et le retire de la liste des sons en cours
        """
        if num < len(self._music_playing):
            self._music_playing[num].terminate()
            self._music_playing.pop(num)

    def stopAllSounds(self):
        u"""
        Arrête tous les sons en cours et les retire de la liste
        """
        [self.stopSound(num) for num in self._music_playing]

    def getMusicPlaying(self):
        """
        Renvoie la liste des threads
        """
        return self._music_playing


if __name__ == "__main__":
    sound = GameSound()
    sound.startInfiniteSound('test.wav')
    while True:
        print(1)
