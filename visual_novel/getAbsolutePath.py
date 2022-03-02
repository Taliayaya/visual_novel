import os


def getAbsolutePath(script_dir: str, rel_path: str) -> str:
    """
    Permet d'indiquer un chemin absolu dans le module à partir chemin
    du dossier et du fichier à accéder. 

    Préconditions: 
        script_dir (str): est le chemin du fichier actuel
        rel_path (str): est le chemin du fichier cible

    Postcondition:
        Renvoie un chemin absolu permettant d'accéder au fichier cible
        à partir du fichier actuel
    """
    return os.path.join(script_dir, rel_path)
