import sqlite3


def main():
    # connexion à la base de donnée 'alesc.sqlite', qui est alors créee si elle n'existe pas encore
    with sqlite3.connect('alesc.sqlite') as connection:
        curseur = connection.cursor()

        # le fichier SQL n'est pas demandé par le TP, mais il était possible de creer la BDD en exécutant le fichier SQL.
        # lire le contenur du fichier alesc SQL contenant les instructions pour créer les tables
        # with open('alesc.sql', 'r') as file:
        #     alesc_sql_script = file.read()
        #     curseur.executescript(alesc_sql_script)

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

        connection.commit()
        curseur.close()


if __name__ == '__main__':
    main()
