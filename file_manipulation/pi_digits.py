# ex1 : Fichier texte

import os
from string import punctuation
from math import pi


def calculate_digits_from_text(chemin: str):
    """
    Calcule les digits d'un nombre qui est de la forme d'un chiffre avec une virgule suivi d'autres chiffres,
    à l'aide d'un texte.
    """
    if not os.path.isfile(chemin):
        raise FileNotFoundError('Ce fichier n\'existe pas.')

    with open(chemin, encoding="utf-8") as file_digits:
        contenu = file_digits.read()
        for p in punctuation:  # OPTIMISATION
            contenu = contenu.replace(p, ' ')
        contenu = contenu.split()
        number_digits = ''
        for mot in contenu:
            number_digits += str(len(mot))
        number_digits = float(number_digits[0] + '.' + number_digits[1:])
        return number_digits


def write_digits_to_file(file_name: str, nb: float):
    '''écrit le nombre résultat dans un fichier'''
    with open(file_name, "w") as file:
        file.write(str(nb))


def main():
    print("\nCalculons les digits de π à l’aide du poème !")
    try:
        nombre = calculate_digits_from_text('poeme.txt')

    except FileNotFoundError as error:
        print(error)

    else:
        if nombre == pi:
            print('Oui le nombre calculé correspond bien à pi !')
            write_digits_to_file('pi_digits.txt', nombre)
            print(f'Le nombre {nombre} est inscrit dans le fichier pi_digits.txt')
        else:
            print('poeme.txt ne représente pas les digits de pi')


if __name__ == '__main__':
    main()
