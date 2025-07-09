class Rectangle:
    '''
    Définition de la classe Rectangle.
    '''

    def __init__(self, longueur: float, largeur: float):
        self.set_longueur(longueur)
        self.set_largeur(largeur)

    def get_longueur(self) -> float:
        return self._longueur

    def set_longueur(self, value: float):
        '''permet de définir la longueur du rectangle et ne retourne rien'''
        if not isinstance(value, float):
            raise TypeError('La longueur doit être un nombre réel. ')
        if value <= 0:
            raise ValueError('Veuillez entrer une longueur positive. ')
        self._longueur = value

    def get_largeur(self) -> float:
        return self._largeur

    def set_largeur(self, value: float):
        '''permet de définir la largeur du rectangle et ne retourne rien'''
        if type(value) != float:
            raise TypeError('La largeur doit être un nombre réel. ')
        if value <= 0:
            raise ValueError('Veuillez entrer une largeur positive. ')
        self._largeur = value

    def perimetre(self) -> float:
        return 2 * (self.get_longueur() + self.get_largeur())

    def aire(self) -> float:
        return self.get_longueur() * self.get_largeur()

    def est_carre(self) -> bool:
        return self.get_longueur() == self.get_largeur()

    def le_plus_grand(self, other: 'Rectangle') -> 'Rectangle':
        '''
        Compare les aires et retourne le plus grand rectangle des 2 passés en paramètre.
        '''
        if self.aire() > other.aire():
            return self
        elif self.aire() < other.aire():
            return other
        # si les 2 sont égaux, arbitrairement nous retournons self
        return self

    def affiche(self):
        '''
        Affichant les caractéristiques d'un rectangle et ne retourne rien.
        '''
        print(
            f'Longueur : [{self.get_longueur()}] - Largeur : [{self.get_largeur()}] - Perimetre : [{self.perimetre()}] - Aire : [{self.aire()}] - ',
            end=' ')
        print("C'est un carre" if self.est_carre() else "Ce n'est pas un carré")


def main():
    print()
    rectangle1 = Rectangle(4.5, 6.9)
    rectangle2 = Rectangle(2.0, 2.0)
    rectangle3 = Rectangle(10.4, 20.7)
    rectangle4 = rectangle2

    print('[Rectangle 1] ', end='')
    rectangle1.affiche()
    print('[Rectangle 2] ', end='')
    rectangle2.affiche()
    print('[Rectangle 3] ', end='')
    rectangle3.affiche()
    print('[Rectangle 4] ', end='')
    rectangle4.affiche()

    print('\nComparons ces rectangles 2 à 2 : quelle est la plus grande aire des deux ? ')
    print(f'1 VS 2 => {rectangle1.le_plus_grand(rectangle2).aire()}')
    print(f'1 VS 3 => {rectangle1.le_plus_grand(rectangle3).aire()}')
    print(f'2 VS 4 => {rectangle2.le_plus_grand(rectangle4).aire()}')
    print(f'3 VS 2 => {rectangle3.le_plus_grand(rectangle2).aire()}')
    print()


if __name__ == '__main__':
    main()
