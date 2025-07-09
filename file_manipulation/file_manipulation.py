# 1/ Fichier texte formaté
import csv
import os
from pathlib import Path
import pickle


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

    def to_dict(self) -> dict:
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

            writer = csv.DictWriter(file, lineterminator="\n",
                                    fieldnames=['nom', 'annee_naissance', 'gpa', 'connais_python'])
            writer.writeheader()  # écriture de la ligne d'entête
            for etudiant in self.liste_etu:
                writer.writerow(etudiant.to_dict())

    @staticmethod
    def charger_csv(chemin: Path) -> 'Groupe':
        """Instancie un objet de type Groupe en lisant un fichier csv"""
        group_charge = Groupe()
        with open(chemin, encoding='utf-8') as file:
            dict_reader = csv.DictReader(file)
            for dict_row in dict_reader:
                group_charge.liste_etu.append(Etudiant.from_dict(dict_row))
        return group_charge


# ce bout de code ci-dessous n'est pas défni dans main2() afin de pouvoir être utilisé dans l'exercice suivant
etu1 = Etudiant('Toto', 2000, 5.0, True)
etu2 = Etudiant('Tata', 2001, 4.4, False)
groupe1 = Groupe()
groupe1.liste_etu.append(etu1)
groupe1.liste_etu.append(etu2)


def main2():
    global groupe1

    chemin = input('entrez le chemin du fichier csv où stocker les données : ')
    groupe1.sauvegarder_csv(chemin)

    groupe2 = Groupe.charger_csv(chemin)

    # comparaison
    print('\nAu départ, le groupe contient ces étudiants :')
    for etu in groupe1.liste_etu:
        print((etu.to_dict()))
    print('\nAprès avoir sauvegardées ces données dans le fichier csv, on charge les données suivantes :')
    for etu in groupe2.liste_etu:
        print((etu.to_dict()))
    print("\nDonc les étudiants de l’objet groupe chargé sont similaires aux étudiants d’origine.")


if __name__ == '__main__':
    main2()


# =======================================================================================================
# Ex 2/ Fichiers binaires


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

# A décommenter si besoin :
# if __name__=='__main__':
#     main3()
