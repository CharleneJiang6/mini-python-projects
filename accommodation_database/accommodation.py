import sqlite3
import pandas as pd


def main():
    with sqlite3.connect('alesc.sqlite') as connexion:
        print("Initialisation de la base de données...")
        curseur = connexion.cursor()
        init_db(connexion, curseur)

        logeurs = pd.read_excel('logeurs.xlsx')
        logements = pd.read_excel('logements.xlsx')
        etudiants = pd.read_excel('etudiants.xlsx')
        insert_db([logeurs, logements, etudiants], connexion, curseur)

        while True:
            print("+---------------------------------------------------------+\n|\n"
                  "|  Entrer un mot-clé pour effectuer une opération :\n|\n"
                  "|  > 'logement' : obtenir des informations sur un logement\n"
                  "|  > 'exit' : quitter le programme\n"
                  "|\n+---------------------------------------------------------+\n")
            choix = input("Mot-clé > ").lower()
            if choix == "logement":
                nom = input("Entrer le nom du logeur : ").lower()
                prenom = input("Entrer le prénom du logeur : ").lower()
                print(info_logement(curseur, (nom, prenom)))
            elif choix == "exit":
                print("\nArrêt du programme...")
                curseur.close()
                exit()
            else:
                print("\nChoix non reconnu. Veuillez rééssayer.\n")


def init_db(connexion: sqlite3.Connection, curseur: sqlite3.Cursor):
    """
    Initialise la base de données à partir des instructions fournies en paramètre
    :param connexion: base de données connectée
    :param curseur: curseur actif
    :return:
    """

    # curseur.executescript permet d'éxecuter plusieurs intructions SQL
    curseur.executescript("""
                DROP TABLE IF EXISTS Logeur;
                DROP TABLE IF EXISTS Logement;
                DROP TABLE IF EXISTS Etudiant;

                CREATE TABLE Logeur
                (
                    id_logeur   INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom         VARCHAR(30) NOT NULL,
                    prenom      VARCHAR(30) NOT NULL,
                    numero_rue  INTEGER     NOT NULL,
                    nom_rue     INTEGER     NOT NULL,
                    code_postal INTEGER     NOT NULL,
                    ville       VARCHAR(30) NOT NULL,
                    UNIQUE (nom, prenom, numero_rue, nom_rue, code_postal, ville)
                );


                CREATE TABLE Logement
                (
                    id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_rue  INTEGER                                                               NOT NULL,
                    nom_rue     INTEGER                                                               NOT NULL,
                    code_postal INTEGER                                                               NOT NULL,
                    ville       VARCHAR(30)                                                           NOT NULL,
                    label       INT,
                    logeur      INT REFERENCES Logeur (id_logeur)                                     NOT NULL,
                    type        VARCHAR(7) CHECK ( type IN ('chambre', 'studio',
                                                            'f1', 'f2', 'f3', 'f4', 'f5', 'maison') ) NOT NULL
                );


                CREATE TABLE Etudiant
                (
                    id_etu   INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom      VARCHAR(30) NOT NULL,
                    prenom   VARCHAR(30) NOT NULL,
                    semestre VARCHAR(4)  NOT NULL,
                    logement INT REFERENCES Logement (id_logement),
                    logeur   INT REFERENCES Logeur (id_logeur)
                );
                """)
    connexion.commit()


def insert_db(sources: list[pd.DataFrame], connexion: sqlite3.Connection, curseur: sqlite3.Cursor) -> None:
    """
    Insère les éléments fournis en source dans la base de données.
    :param sources: tableau de sources contenant des
    fichiers Excel lus par Pandas (de la forme [logeurs, logements, etudiants])
    :param connexion: base de données connectée
    :param curseur: curseur actif
    """

    # logeurs
    for index, row in sources[0].iterrows():
        curseur.execute("""
                    INSERT INTO Logeur (nom, prenom, numero_rue, nom_rue, code_postal, ville) VALUES (?,?,?,?,?,?)""",
                        tuple(row))

    # logements
    for index, row in sources[1].iterrows():

        req_id_logueur = "SELECT l.id_logeur FROM Logeur l WHERE (l.nom =:nom AND l.prenom =:prenom )"
        curseur.execute(req_id_logueur,
                        {"nom": row.nom_logeur, "prenom": row.prenom_logeur})

        resultat = curseur.fetchone()
        if not resultat:
            raise ValueError('Logeur non trouvé')
        id_logeur = resultat[0]

        curseur.execute("""
            INSERT INTO Logement (numero_rue, nom_rue, code_postal, ville, label, logeur, type) VALUES (?,?,?,?,?,?,?)""",
                        (*row[0:5], id_logeur, row.iloc[7]))  # unpacking sur les premiers valeurs de la ligne

    # étudiants
    for index, row in sources[2].iterrows():
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

    connexion.commit()


def info_logement(curseur: sqlite3.Cursor, logeur: tuple[str, str]):
    """
    Permet d'obtenir des informations sur les logements d'un logeur.
    :param curseur: curseur actif
    :param logeur: tuple contenant le nom et prénom du logeur
    :return: str formaté (prêt à être print) contenant les infos des logements
    """
    # on sélectionne tous les logements ayant le logeur passé en paramètre
    curseur.execute("SELECT * FROM Logement WHERE logeur = (SELECT id_logeur FROM Logeur WHERE nom =? AND prenom = ?)",
                    logeur)
    results = curseur.fetchall()
    affichage = (f"\n+---------------------------------------------------------+\n"
                 f"| Logeur : {logeur[0].title()} {logeur[1].title()}\n"
                 f"+---------------------------------------------------------+\n")

    # on parcourt chaque logement, puis on sélectionne chaque étudiant étant dans ce logement
    for index, result in enumerate(results):
        curseur.execute("SELECT nom, prenom FROM Etudiant WHERE logement =:id_log", {'id_log': result[0]})
        noms = curseur.fetchall()

        # on ajoute les infos du logement à la réponse formatée
        affichage += (f"| ({result[7]} | {'*' * result[5] if result[5] != 0 else '0'}) Logement n°{index + 1} : "
                      f"{result[1]} rue {result[2].title()}, {result[3]} {result[4].title()}\n")
        # on ajoute les infos de chaque étudiant du logement à la réponse, en-dessous des infos du logement
        for idx2, nom in enumerate(noms):
            affichage += f"|   > Étudiant n°{idx2 + 1} : {nom[0].title()} {nom[1].title()}\n"
        # on indique si aucun étudiant n'est dans le logement
        if len(noms) == 0:
            affichage += f"|   > Ce logement est vide.\n"
        affichage += f"+---------------------------------------------------------+\n"
    # s'il n'y a aucun logement trouvé, on écrit autre chose
    if len(results) == 0:
        affichage += (f"| Cette personne n'a aucun logement en location.\n"
                      f"+---------------------------------------------------------+\n")
    return affichage


if __name__ == '__main__':
    main()
