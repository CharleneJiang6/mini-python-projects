import sqlite3


def main():
    with sqlite3.connect('alesc.sqlite') as connection:
        curseur = connection.cursor()

        nom, prenom = input('\nEntrez le nom du logeur : ').lower(), input('Entrez le prenom du logeur : ').lower()

        curseur.execute("""
            SELECT 
            lgmt.id_logement,
            lgmt.numero_rue,
            lgmt.nom_rue,
            lgmt.code_postal,
            lgmt.ville,
            lgmt.label,
            lgmt.type
            FROM Logement lgmt
                     JOIN Logeur l ON lgmt.logeur = l.id_logeur
            WHERE l.nom = ?
            AND l.prenom = ?;""",
                        (nom, prenom))

        # vérifier si ce logeur recherché possède des logements
        logements = curseur.fetchall()
        if not logements:
            raise ValueError('\nCe logeur n\'existe pas ou ne possède pas de logements.')

        curseur.execute("""
            SELECT 
                e.logement,
                e.nom,
                e.prenom
            FROM Etudiant e
                     JOIN Logement lgmt ON lgmt.id_logement = e.logement
                     JOIN Logeur l ON e.logeur = l.id_logeur
            WHERE l.nom = ?
            AND l.prenom = ?;""",
                        (nom, prenom))

        etudiants = curseur.fetchall()

        print(f"\nNom du logeur : {nom.title()} {prenom.title()}")

        for logement in range(len(logements)):
            print(f"\nLogement {logement + 1} : {logements[logement][1]} rue", end=" ")
            for val in logements[logement][2:5]:
                print(str(val).title(), end=" ")
            print(f"{'*' * logements[logement][5] if logements[logement][5] != 0 else ' '} ({logements[logement][6]})")
            # print()
            for etu in etudiants:
                if etu[0] == logements[logement][0]:
                    print(f"\tNom de l'étudiant : {etu[1].title()} {etu[2].title()}")

        curseur.close()


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        print(error)
    finally:
        print('\nFin de la recherche.')
