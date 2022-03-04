# Les motifs

Afin de détecter les différentes parties d'un texte et leurs métadonnées, ce fichier à pour but de regrouper les différents symboles et structures nécessaires à la construction de l'histoire.

## Présence d'un choix

### Signification des symboles

| Symbole | Role                                 |
| ------- | ------------------------------------ |
| #       | Délimite le début du choix           |
| \|      | Délimite le choix 1 du choix 2       |
| $       | Délimite la fin du choix             |
| ~       | Correspond à la destination du choix |

### Exemple

```
Did you ever hear the Tragedy of Darth Plagueis the Wise ?
#No~dewit.txt|...~tragedy.txt$
```

### Traduction de l'exemple :

Did you ever hear the Tragedy of Darth Plagueis the Wise ?

-   Choix 1 : No -> emmène vers dewit.txt
-   Choix 2 : ... -> emmène vers tragedy.txt

## Présence d'un dialogue 

### Signification des symboles 

| Symbole | Role                                 |
| ------- | ------------------------------------ |
| -       | Indique le début d'un dialogue       |
| : -     | Délimite interlocuteur/texte         |

### Exemple

```
- Palpatine : - "Did you ever hear the Tragedy of Darth Plagueis the Wise ?"
```
```
{"type":"dialogue", "name":"Palpatine", "text":'"Did you ever hear the Tragedy of Darth Plagueis the Wise ?"'}
```


