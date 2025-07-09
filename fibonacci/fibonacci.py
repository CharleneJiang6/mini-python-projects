from time import sleep


def cache(func):
    """
    Décorateur qui permet de placer en cache des résulats d'une fonction
    :return: le résultat caché, sinon le résultat calculé puis caché par la suite
    """
    dic_cache = {}

    def wrapper(param):
        if param not in dic_cache:
            dic_cache[param] = func(param)
            return func(param)
        return dic_cache[param]

    return wrapper


@cache
def func_slow(param: int) -> str:
    """
    Simulation d'une fonction coûteuse en temps et qui fait de l'affichage.
    :return: Une chaine de caractère
    """
    sleep(param)
    return 'Fin de ma fonction'


def fibonacci_recursif(nb: int) -> int:
    """
    Calcule la valeur n de la suite Fibonacci de manière recursive.
    """
    if nb == 0:
        return 0
    elif nb == 1:
        return 1
    return fibonacci_recursif(nb - 1) + fibonacci_recursif(nb - 2)


def fibonacci_iteratif(nb: int) -> list:
    """
    Calcule la prochaine valeur de la suite fibonacci de manière itérative.
    :return: La liste représentant la suite fibonacci
    """
    suite_fibo = [0, 1]
    for i in range(2, nb + 1):
        suite_fibo.append(suite_fibo[i - 1] + suite_fibo[i - 2])
    return suite_fibo


@cache
def fibonacci_recursif_cache(nb: int) -> int:
    """
    Calcule la valeur n de la suite Fibonacci de manière récursive, mais avec le décorateur @cache cette fois-ci
    """
    if nb == 0:
        return 0
    elif nb == 1:
        return 1
    return fibonacci_recursif_cache(nb - 1) + fibonacci_recursif_cache(nb - 2)


def main():
    from timeit import timeit
    print("\nVérification de la suite fibonacci récursive : ")
    print([fibonacci_recursif(number) for number in range(11)])

    print('\nTemps d\'exécution de fibonacci_recursif(35) : ',
          timeit('fibonacci_recursif(35)', globals=globals(), number=1))
    print('Temps d\'exécution de fibonacci_recursif(36) : ',
          timeit('fibonacci_recursif(36)', globals=globals(), number=1))
    # Suite à la comparaison des durées, on remarque que fibonacci_recursif(36) prend plus de temps pour calculer,
    # que pour fibonacci_recursif(35). L'un prend 4 secondes et l'autre prend deux secondes.

    print("\nVérification de la suite fibonacci itérative : ")
    print(fibonacci_iteratif(10))

    print('\nTemps d\'exécution de fibonacci_iteratif(35) : ',
          timeit('fibonacci_iteratif(35)', globals=globals(), number=1))
    print('Temps d\'exécution de fibonacci_iteratif(36) : ',
          timeit('fibonacci_iteratif(36)', globals=globals(), number=1))
    # Remarquons que cette fois-ci, les calculs de fibonacci_iteratif est bien plus rapide que fibonacci_recursif, de l'ordre de e-05 seconde

    # Calcul des durées d'exécution avec fibonacci_recursif_cache
    print('\nFibonacci récursive avec cache :')
    print('Temps d\'exécution de fibonacci_recursif_cache(35) : ',
          timeit('fibonacci_recursif_cache(35)', globals=globals(), number=1))
    print('Temps d\'exécution de fibonacci_recursif_cache(36) : ',
          timeit('fibonacci_recursif_cache(36)', globals=globals(), number=1))
    # On remarque que grâce au cache, on a une fonction fibonacci recursive qui calcule quasiment à la même vitesse que la fonction itérative : cela passe de 4 secondes à l'ordre de e-05 seconde
    # Par contre fibonacci_iteratif(35) est un tout petit plus rapide que fibonacci_recursif_cache(35)
    # Cependant la vitesse, de calcul de fibo(36) avec cache, est un tout légèrement plus rapide que fibo(36) itératif, ce qui montre donc tout l'intérêt du cache.
    print()


if __name__ == '__main__':
    main()
