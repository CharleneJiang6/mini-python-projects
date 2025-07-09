#  ex 3 : fichiers binaires

import pickle


def save_groupe_to_binary_file(chemin:str, objet:any):
    """Sauvegarder un objet dans un fichier binaire."""
    with open(chemin, "wb") as file_destination:
        pickle.dump(objet, file_destination)


def load_binary_file(chemin):
    """Charger les données binaires sauvegardées"""
    with open(chemin, "rb") as file:
        return pickle.load(file)


# Q2 : Quels avantages et désavantage voyez‑vous à l’utilisation du mode texte ou binaire ?

# Les avantages du mode texte sont les suivants : les données écrites et lues dans ces fichiers nous sont lisibles.
# Ainsi, il est facile pour nous de les manipuler, avec un éditeur de texte par exemple.
# Par ailleurs, on peut contrôler la quantité de données à lire, à l'aide des fonctions lisant une ou
# plusieurs lignes/caractères.
# Un des inconvénients du fichier texte est que tout objet sera transformé en texte, et donc si on veut faire des
# manipulations sur les données, numériques notamment,
# provenant du fichier texte, il faut les revconvertir dans le type désiré, comme dans notre fonction Etudiant.from_dict().
# De même, le fichier texte n'est pas très pratique pour stocker des données complexes. De plus, pour pouvoir lire les
# caractères spéciaux, il ne faut pas oublier d'utiliser les encodages comme UTF-8.

# Quant aux fichiers binaires, le plus grand avantage réside dans la facilité et la rapidité de manipulation ;
# l'écriture et la lecture se fait avec dump et load respectivement.
# Alors qu'avec le fichier texte, on a dû définir plusieurs fonctions avant, comme vu plus haut dans les
# classes Etudiant et Groupe.
# Il est plus facile de stocker des données complexes, ou un objet entier, comme avec notre objet Groupe d'étudiants
# de tout à l'heure.
# Toutefois, le contenu dans un fichier binaire nous est illisible : les données sont plein de caractères
# spéciaux successifs.
# Ainsi, manipuler des données binaires peut parfois être délicat.
# Donc les fichiers binaires sont sont très adaptés pour sérialiser et désérialiser des objets, dans le but de les
# sauvegarder ou de les échanger avec d’autres programmes.

