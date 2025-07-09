from random import randint


class Pokemon:
    """Classe mère Pokemon permettant de créer des objets enfants Pokemon."""

    def __init__(self, nom: str, pv: int, atk: int):
        self.nom = nom
        self.pv = pv
        self.atk = atk

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value: str):
        if type(value) != str:
            raise TypeError('Le nom doit être une chaine. ')
        self._nom = value

    @property
    def pv(self):
        return self._pv

    @property
    def atk(self):
        return self._atk

    @pv.setter
    def pv(self, value: int):
        if type(value) != int:
            raise TypeError('Le point de vie est un entier. ')
        if value < 0:
            raise ValueError('Le point de vie est un entier positif. ')
        self._pv = value

    @atk.setter
    def atk(self, value: int):
        if type(value) != int:
            raise TypeError('Le point de dégât est un entier. ')
        if value < 0:
            raise ValueError('Le point de dégât est un entier positif. ')
        self._atk = value

    @property
    def est_ko(self) -> bool:
        """Retourne si un Pokémon est vaincu, autrement dit, il ne possède plus de points de vie."""
        return self.pv == 0

    def attaquer(self, autre: 'Pokemon') -> None:
        """
        Cette méthode permet au Pokémon self d'attaquer un autre, en lui retirant un certain nombre de points de vie
        """

        # La valeur totale d'attaque est l'entier pioché aléatoirement multiplié par le multiplicateur.
        # Autrement dit, en fonction du type du Pokemon adversaire, mon dégat est plus ou moins fort.
        val_attack = int(self.calc_multiplicateur(autre) * randint(0,
                                                                   self.atk))  # conversion en entier car le multiplicateur peut être égale à 0.5
        if val_attack >= autre.pv:
            autre.pv = 0
        else:
            autre.pv -= val_attack

    def combattre(self, autre: 'Pokemon') -> tuple['Pokemon', int]:
        """
        Cette méthode permet aux deux Pokémon self et autre de s'attaquer à tour de rôle.
        :return: Le gagnant et le nombre de tours d'attaque
        """
        tour = 0
        while not self.est_ko and not autre.est_ko:
            tour += 1

            self.attaquer(autre)
            if autre.est_ko:
                return self, tour

            autre.attaquer(self)
            if self.est_ko:
                return autre, tour

    def __str__(self) -> str:
        return f'Nom : {self.nom} / Points de vie : {self.pv} / Points de dégâts : {self.atk}'


# Héritage : Definition de 4 classes filles de Pokemon

class PokemonNormal(Pokemon):

    def __init__(self, nom: str, pv: int, atk: int):
        super().__init__(nom, pv, atk)

    def calc_multiplicateur(self, other) -> int:
        '''
        Les Pokémons normaux infligent et reçoivent des dégâts normaux de tous les types
        :return: 1
        '''
        if type(other) in [PokemonFeu, PokemonEau, PokemonPlante, PokemonNormal]:
            return 1


class PokemonFeu(Pokemon):
    def __init__(self, nom: str, pv: int, atk: int):
        super().__init__(nom, pv, atk)

    def calc_multiplicateur(self, other: Pokemon) -> int:
        '''
        Les Pokémons feu font deux fois plus de dégâts aux Pokémons plante mais font deux fois moins de dégâts aux Pokémons eau ou feu
        :return: 0.5 ou 1 ou 2
        '''
        if type(other) == PokemonPlante:
            return 2
        elif type(other) == (PokemonEau or PokemonFeu):
            return 0.5
        elif type(other) == PokemonNormal:
            return 1


class PokemonEau(Pokemon):
    def __init__(self, nom: str, pv: int, atk: int):
        super().__init__(nom, pv, atk)

    def calc_multiplicateur(self, other) -> float:
        '''
        Les Pokémons eau font deux fois plus de dégâts aux Pokémons feu mais font deux fois moins de dégâts aux Pokémons eau ou plante.
        :return: 0.5 ou 1 ou 2.
        '''
        if type(other) == PokemonFeu:
            return 2.0
        elif type(other) == (PokemonEau or PokemonPlante):
            return 0.5
        elif type(other) == PokemonNormal:
            return 1.0


class PokemonPlante(Pokemon):
    def __init__(self, nom: str, pv: int, atk: int) -> None:
        super().__init__(nom, pv, atk)

    def calc_multiplicateur(self, other):
        '''
        Les Pokémons plante font deux fois plus de dégâts aux Pokémons eau mais font deux fois moins de dégâts aux Pokémons plante ou feu.
        :return: 0.5 ou 1 ou 2
        '''
        if type(other) == PokemonEau:
            return 2
        elif type(other) in [PokemonFeu, PokemonPlante]:
            return 0.5
        elif type(other) == PokemonNormal:
            return 1


def main():
    try:
        pokemon1 = PokemonFeu('Feu', 1000, 50)
        pokemon2 = PokemonEau('Eau', 500, 100)
        pokemon3 = PokemonPlante('Plante', 20, 30)
        pokemon4 = PokemonNormal('Normal', 50, 51)

        print(pokemon1)
        print(pokemon2)
        print(pokemon3)
        print(pokemon4)

    except TypeError as e:
        print(e)
    except ValueError as e:
        print(e)

    else:
        print()
        gagnant1, nb_tour = pokemon1.combattre(pokemon2)
        print(f'combat 1 : {pokemon1.nom} VS {pokemon2.nom}. Gagnant => {gagnant1.nom}, en {nb_tour} tours')

        gagnant2, nb_tour = pokemon4.combattre(pokemon3)
        print(f'combat 2 : {pokemon4.nom} VS {pokemon3.nom}. Gagnant => {gagnant2.nom}, en {nb_tour} tours')


if __name__ == '__main__':
    main()
