import pandas as pd
import sqlite3


def main():
    with sqlite3.connect('alesc.sqlite') as connection:
        curseur = connection.cursor()

        # on récupère les données des fichiers excels grâce à pandas
        logeurs = pd.read_excel('logeurs.xlsx')
        logements = pd.read_excel('logements.xlsx')
        etudiants = pd.read_excel('etudiants.xlsx')

        # remplissage de la table Logeurs
        # itérer sur chaque ligne du dataframe récupéré, puis insérer chaque ligne dans la BDD
        for index, row in logeurs.iterrows():
            curseur.execute("""
            INSERT INTO Logeur (nom, prenom, numero_rue, nom_rue, code_postal, ville) VALUES (?,?,?,?,?,?)""",
                            tuple(row))
            # chaque valeur dans le tuple(row) remplacera respectivement un "point d'interrogation"

        # remplissage de la table Logements
        for index, row in logements.iterrows():
            req_id_logueur = "SELECT l.id_logeur FROM Logeur l WHERE (l.nom =:nom AND l.prenom =:prenom )"
            curseur.execute(req_id_logueur,
                            {"nom": row.nom_logeur, "prenom": row.prenom_logeur})
            # dans la requête SQL, la valeur d'une variable précédé par deux-points sera issue du dictionnaire
            # passé en paramètre de curseur.execute()
            resultat = curseur.fetchone()
            if not resultat:
                raise ValueError('Logeur non trouvé')
            id_logeur = resultat[0]

            curseur.execute("""
            INSERT INTO Logement (numero_rue, nom_rue, code_postal, ville, label, logeur, type) VALUES (?,?,?,?,?,?,?)""",
                            (*row[0:5], id_logeur, row.iloc[7]))  # unpacking sur les premiers valeurs de la ligne

        # remplissage de la table Etudiants
        for index, row in etudiants.iterrows():
            req_id_logement = """SELECT lo.id_logement, lo.logeur FROM Logement lo
                                        WHERE (lo.numero_rue =? AND lo.nom_rue =? AND lo.code_postal =? AND lo.ville =?)"""
            curseur.execute(req_id_logement,
                            (row.numero_rue, row.nom_rue, row.code_postal, row.ville))

            # ou bien en mode nommé : dico en paramètre de curseur.execute()
            # req_id_logement = """SELECT lo.id_logement, lo.logeur FROM Logement lo
            #                     WHERE (lo.numero_rue =:num AND lo.nom_rue =:nom AND lo.code_postal =:code AND lo.ville =:ville)"""
            # curseur.execute(req_id_logement,
            #                 {"num": row.numero_rue, "nom": row.nom_rue, "code": row.code_postal, "ville": row.ville})

            resultat = curseur.fetchone()
            if not resultat:
                raise ValueError("Pas de logement trouvé pour l'étudiant.")
            id_logement, id_logeur = resultat

            curseur.execute("""
            INSERT INTO Etudiant (nom, prenom, semestre, logement, logeur) VALUES (?,?,?,?,?)""",
                            (*row[0:3], id_logement, id_logeur))

        connection.commit()

        curseur.close()

        print("\nBase de donnée ALESC correctement remplie.")


if __name__ == '__main__':
    main()
