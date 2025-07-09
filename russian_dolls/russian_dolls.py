class PoupeeRusse:
    """
    Classe permettant de créer des poupées russes de différentes tailles et de les emboiter.
    """

    def __init__(self, nom: str, taille: int):

        if type(taille) != int:
            raise TypeError('La taille doit être un entier. ')
        if taille <= 0:
            raise ValueError('La taille doit être positve. ')

        self._taille = taille
        self.nom = nom
        self._est_ouverte = False
        self._dans = None
        self._contient = None

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, value: str):
        if type(value) != str:
            raise TypeError('Le nom doit être une chaine. ')
        self._nom = value

    @property
    def taille(self) -> int:
        return self._taille

    @property
    def est_ouverte(self) -> bool:
        return self._est_ouverte

    @property
    def dans(self) -> 'PoupeeRusse':
        return self._dans

    @property
    def contient(self) -> 'PoupeeRusse':
        return self._contient

    @property
    def est_fermee(self) -> bool:
        return not self.est_ouverte

    @property
    def est_vide(self) -> bool:
        return self.contient == None

    @property
    def est_contenue(self) -> bool:
        return self.dans != None

    def ouvrir(self):
        """permet d'ouvrir une poupée et ne retourne rien"""
        if self.est_fermee and not self.est_contenue:
            self._est_ouverte = True

    def fermer(self):
        """permet de fermer une poupée et ne retourne rien"""
        if self.est_ouverte and self.est_contenue == False:
            self._est_ouverte = False

    def placer_dans(self, poupee: 'PoupeeRusse'):
        """place la poupée self dans la poupée poupee et ne retourne rien"""
        if (not self.est_contenue) and (poupee.est_vide) and (self.est_fermee) and (poupee.est_ouverte) and (
                poupee.taille > self.taille):
            self._dans = poupee
            poupee._contient = self
        # use RAISE ...

    def sortir(self):
        """sort la poupée courante d'une autre poupée et ne retourne rien"""
        if self.dans.est_ouverte and self.est_contenue:
            self._dans._contient = None
            self._dans = None
        else:  # use RAISE insted
            print('Il faut avoir ouvert la poupée extérieure avant de faire sortir celle intérieure.')

    def __str__(self) -> str:
        infos = f'Poupée nommée : {self.nom}, de taille : {self.taille}, '

        if self._est_ouverte:
            infos += 'est ouverte, '
        else:
            infos += 'est fermée, '

        if self.dans is None:
            infos += "n'est pas à l'intérieur d'une autre poupée, "
        else:
            infos += f'contenue dans {self.dans.nom}, '

        if self.contient is None:
            infos += 'et ne contient rien. '
        else:
            infos += f'et contient la poupée {self.contient.nom}. '

        return infos


def main():
    try:
        poupee1 = PoupeeRusse('Anna', 1)
        poupee2 = PoupeeRusse('Barba', 3)
        poupee3 = PoupeeRusse('Carl', 6)

    except TypeError as e:
        print(e)

    except ValueError as e:
        print(e)

    else:
        poupee1.ouvrir()
        poupee2.ouvrir()
        poupee3.ouvrir()

        # Test validé : poupee3 ne rentre bien pas dans poupee1
        # poupee3.placer_dans(poupee1)
        # print(poupee1)
        # print(poupee3)

        poupee1.fermer()
        poupee1.placer_dans(poupee2)
        poupee2.fermer()
        # print(poupee2)
        poupee2.placer_dans(poupee3)
        poupee3.fermer()

        print(poupee1)
        print(poupee2)
        print(poupee3)

        poupee3.ouvrir()
        poupee2.sortir()
        poupee2.ouvrir()
        poupee1.sortir()

        print()
        print(poupee1)
        print(poupee2)
        print(poupee3)

if __name__=='__main__':
    main()
