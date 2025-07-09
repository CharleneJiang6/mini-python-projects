def nb_min(password: str) -> int:
    """
    Calcule le nombre de lettres minuscules dans le mot de passe passé en paramètre.
    :param password: mot de passe à tester
    """
    compteur_car_min = 0
    for caractere in password:
        if caractere.islower():
            compteur_car_min += 1

    return compteur_car_min


def nb_maj(password: str) -> int:
    """
    Calcule le nombre de lettres majuscules dans le mot de passe passé en paramètre.
    """
    compteur_car_maj = 0
    for caractere in password:
        if caractere.isupper():
            compteur_car_maj += 1

    return compteur_car_maj
    #  return len([c for c in password if c.isupper()])


def nb_non_alpha(password: str) -> int:
    """
    Calcule le nombre de caractères non alphabétiques dans le mot de passe passé en paramètre.
    """
    nb_non_alpha = 0
    for caractere in password:
        if not caractere.isalpha():
            nb_non_alpha += 1
    return nb_non_alpha


def long_min(password: str) -> int:
    """
    Retourne la longueur de la plus longue séquence de lettres minuscules présente dans le mot de passe
    """
    longueur_max = 0
    longueur_actuelle = 0
    for caractere in password:
        if caractere.islower():
            longueur_actuelle += 1
            if longueur_actuelle > longueur_max:
                longueur_max = longueur_actuelle
        else:
            longueur_actuelle = 0

    return longueur_max


def long_maj(password: str) -> int:
    """
    Calcule la longueur de la plus longue séquence de lettres majuscules présente dans le mot de passe
    """
    longueur_max = 0
    longueur_actuelle = 0
    for caractere in password:
        if caractere.isupper():
            longueur_actuelle += 1
            if longueur_actuelle > longueur_max:
                longueur_max = longueur_actuelle
        else:
            longueur_actuelle = 0

    return longueur_max


def score(password: str) -> int:
    """
    Calcule le score du mot de passe, qui est défini selon plusieurs critères de bonus et de pénalité
    """

    # Bonus : critères apportant des points
    longueur_password = len(password)
    critere_majuscule = (len(password) - nb_maj(password)) * 2
    critere_minuscule = (len(password) - nb_min(password)) * 3
    critere_non_alpha = nb_non_alpha(password) * 5

    # Pénalités : critères enlevant des points
    plus_grande_sequence_min = long_min(password) * 2
    plus_grande_sequence_maj = long_maj(password) * 3

    return longueur_password + critere_majuscule + critere_minuscule + \
        critere_non_alpha - plus_grande_sequence_min - plus_grande_sequence_maj


def main() -> None:
    print("\nCalcul du score d'un mot de passe")
    password = input("Veuillez entrer un mot de passe : ")
    score_password = score(password)
    if score_password < 20:
        print(f'TRES FAIBLE : le mot de passe {password} a un score de {score_password}')
    elif score_password < 40:
        print(f'FAIBLE : le mot de passe {password} a un score de {score_password}')
    elif score_password < 80:
        print(f'FORT : le mot de passe {password} a un score de {score_password}')
    else:
        print(f'TRES FORT : le mot de passe {password} a un score de {score_password}')
    print()


if __name__ == '__main__':
    main()
