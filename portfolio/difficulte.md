# Difficulté

## Réalisation du moteur de jeu

### Fonctionnement du GUI via tkinter

La réalisation du GUI via Tkinter nécessitait de savoir bricoler un peu. En effet, Tkinter permet de faire une interface graphique statique, c'est-à-dire qu'une fois le root.mainloop() lancé, plus rien après ne peut s'exécuter. Il fallait donc trouver un moyen de pouvoir faire avancer le jeu, simuler des loops for. De plus, l'utilisation d'une class pour faire un moteur de jeu permet d'organiser le code et de le simplifier, cependant les éléments à l'intérieur des méthodes ne pouvait pas en sortir et être accédé depuis d'autres.

### Images

De même, permettre d'afficher des images de fond et des personnages a causé de nombreux soucis d'affichage, donnant des images blanches ou bien sans transparence. 

## Musiques

Le lancement et surtout l'arrêt des musiques a été compliqué puisque le module utilisé pour le lancement des musiques ne permettait pas de couper les musiques. Il a donc fallu bricoler avec des threads pour mettre en pause les musiques.