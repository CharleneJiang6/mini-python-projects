# ex1 : Fichier texte
from string import punctuation
from math import pi


def main1():
    """calculons les digits de π à l’aide d’un poème """
    with open('poeme.txt', encoding="utf-8") as file:
        contenu = file.read()
        for caractere in contenu:
            if caractere in punctuation:
                contenu = contenu.replace(caractere, ' ')
        contenu = contenu.split()
        # print(contenu)
        pi_digits = ''
        for mot in contenu:
            pi_digits += str(len(mot))
        pi_digits = float(pi_digits[0] + '.' + pi_digits[1:])
        if pi_digits == pi:
            print(f'C\'est correct, pi vaut : {pi_digits}')
        # else:
        #     # pour les verif
        #     print(f'Voici la valeur calculé : {pi_digits}')
        #     print(f'Voici la valeur reelle : {pi}')

        with open("pi_digits.txt","w") as file2:
            file2.write(str(pi_digits))
            print('Pi est écrit dans le fichier "pi_digits.txt"')


# if __name__=='__main__':
#     main1()


# ======================================================================================================================
# ex2: Fichier texte formaté
import csv
import os
from pathlib import Path


class Etudiant:
    """Classe permettant de créer un objet Etudiant."""

    def __init__(self, nom: str, annee_naissance: int, gpa: float, connais_python: bool):
        self._nom = nom
        self._annee_naissance = annee_naissance
        self._gpa = gpa
        self._connais_python = connais_python

    @property
    def nom(self):
        return self._nom

    @property
    def annee_naissance(self):
        return self._annee_naissance

    @property
    def gpa(self):
        return self._gpa

    @property
    def connais_python(self):
        return self._connais_python


    def to_dict(self)->dict:
        """retourne un dictionnaire décrivant l’objet de type Etudiant"""
        return {'nom': self.nom, 'annee_naissance': self.annee_naissance, 'gpa': self.gpa,
                'connais_python': self.connais_python}


    @staticmethod
    def from_dict(dico_etu: dict) -> 'Etudiant':
        """Instancie un objet de type Etudiant à partir d'un dictionnaire de même format que celui produit par Etudiant.to_dict
        :param dico_etu: un dictionnaire réprésentant un étudiant de même format que celui produit par Etudiant
        """
        annee_naissance = int(dico_etu['annee_naissance'])
        gpa = float(dico_etu['gpa'])
        # vérifier si connais_python vaut False; sinon le convertir directement avec bool() retournerai toujours True
        if dico_etu['connais_python'] == 'False':
            connais_python = False
        else:
            connais_python = bool(dico_etu['connais_python'])
        return Etudiant(dico_etu['nom'], annee_naissance, gpa, connais_python)


class Groupe:
    """Classe permettant de créer un objet Groupe qui contient une liste d'Etudiants."""

    def __init__(self):
        self._liste_etu = []

    @property
    def liste_etu(self):
        return self._liste_etu

    def sauvegarder_csv(self, chemin: Path) -> None:
        """Sauvegarde le contenu d'un objet Etudiant dans un fichier csv"""

        with open(chemin, "w") as file:
            if not os.path.isfile(chemin):
                raise FileNotFoundError('Le chemin ne correspond à aucun fichier.')

            writer = csv.DictWriter(file,lineterminator="\n", fieldnames=['nom', 'annee_naissance', 'gpa', 'connais_python'])
            writer.writeheader()  #écriture de la ligne d'entête
            for etudiant in self.liste_etu:
                writer.writerow(etudiant.to_dict())


    @staticmethod
    def charger_csv(chemin: Path)->'Groupe':
        """Instancie un objet de type Groupe en lisant un fichier csv"""
        group_charge = Groupe()
        with open(chemin, encoding='utf-8') as file:
            dict_reader = csv.DictReader(file)
            for dict_row in dict_reader:
                group_charge.liste_etu.append(Etudiant.from_dict(dict_row))
        return group_charge


# ce bout de code ci-dessous n'est pas défni dans main2() afin de pouvoir être utilisé dans l'exercice 3
etu1 = Etudiant('Toto', 2000, 5.0, True)
etu2 = Etudiant('Tata', 2001, 4.4, False)
groupe1 = Groupe()
groupe1.liste_etu.append(etu1)
groupe1.liste_etu.append(etu2)


def main2():
    global groupe1

    chemin = input('entrez le chemin du fichier csv où stocker les données : ')
    groupe1.sauvegarder_csv(chemin)

    groupe2=Groupe.charger_csv(chemin)

    #comparaison
    print('\nAu départ, le groupe contient ces étudiants :')
    for etu in groupe1.liste_etu:
        print((etu.to_dict()))
    print('\nAprès avoir sauvegardées ces données dans le fichier csv, on charge les données suivantes :')
    for etu in groupe2.liste_etu:
        print((etu.to_dict()))
    print("\nDonc les étudiants de l’objet groupe chargé sont similaires aux étudiants d’origine.")


if __name__ == '__main__':
    main2()


# ======================================================================================================================
#  ex 3 : fichiers binaires

import pickle


def main3():
    global groupe1
    # Sauvegarder le groupe d'étudiants de l'exercice 2
    with open("liste_etu.pkl", "wb") as file:
        pickle.dump(groupe1, file)

    # Charger le groupe d'étudiants qu'on vient de sauvegarder
    with open("liste_etu.pkl", "rb") as file:
        contenu = pickle.load(file)
        print("\nComparons les données chargées et les données initiales !")
        print("Voici ce que nous avons au départ : ")
        for etu in groupe1.liste_etu:
            print((etu.to_dict()))
        print("\nEt voici les données chargées du fichier binaire : ")
        for etu in contenu.liste_etu:
            print((etu.to_dict()))
        print("\nLes données sont exactement similaires !")


# if __name__=='__main__':
#     main3()


# Q2 : Quels avantages et désavantage voyez‑vous à l’utilisation du mode texte ou binaire ?

# Les avantages du mode texte sont les suivants : les données écrites et lues dans ces fichiers nous sont lisibles. Ainsi, il est facile pour nous de les manipuler, avec un éditeur de texte par exemple.
# Par ailleurs, on peut contrôler la quantité de données à lire, à l'aide des fonctions lisant une ou plusieurs lignes/caractères.
# Un des inconvénients du fichier texte est que tout objet sera transformé en texte, et donc si on veut faire des manipulations sur les données, numériques notamment,
# provenant du fichier texte, il faut les revconvertir dans le type désiré, comme dans notre fonction Etudiant.from_dict().
# De même, le fichier texte n'est pas très pratique pour stocker des données complexes. De plus, pour pouvoir lire les caractères spéciaux, il ne faut pas oublier d'utiliser les encodages comme UTF-8.

# Quant aux fichiers binaires, le plus grand avantage réside dans la facilité et la rapidité de manipulation ; l'écriture et la lecture se fait avec dump et load respectivement.
# Alors qu'avec le fichier texte, on a dû définir plusieurs fonctions avant, comme vu plus haut dans les classes Etudiant et Groupe.
# Il est plus facile de stocker des données complexes, ou un objet entier, comme avec notre objet Groupe d'étudiants de tout à l'heure.
# Toutefois, le contenu dans un fichier binaire nous est illisible : les données sont plein de caractères spéciaux successifs.
# Ainsi, manipuler des données binaires peut parfois être délicat.
# Donc les fichiers binaires sont sont très adaptés pour sérialiser et désérialiser des objets, dans le but de les sauvegarder ou de les échanger avec d’autres programmes.

