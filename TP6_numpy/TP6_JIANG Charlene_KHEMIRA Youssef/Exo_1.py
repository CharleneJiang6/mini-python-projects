import numpy as np
import scipy
import matplotlib.pyplot as plt


def main():
    temperature = np.load('temperatures.npy')
    # temperature est alors une liste de tuples (temp_reelle, v_mesuree)
    temp_reelle = [t[0] for t in temperature]
    v_mesuree = [t[1] for t in temperature]
    temp_estimee = [10 * v - 10 for v in v_mesuree]
    # plt.close("all")

    # figure contenant les courbes des températures
    fig_temperatures = plt.figure()
    ax1 = fig_temperatures.add_subplot()
    ax1.plot(temp_reelle, 'b', label="Réelle")
    ax1.plot(temp_estimee, 'r', label="Estimée")

    # figure contenant les histogrammes d'erreurs
    fig_erreurs = plt.figure()

    ax2 = fig_erreurs.add_subplot()
    ax2.hist(temp_estimee, label="T° estimée")
    print(f"L'erreur quadratique moyenne vaut : {rmse(v_mesuree, temp_reelle)}")

    v_lissee = scipy.signal.medfilt(v_mesuree, 13)
    t_lissee = [10 * v - 10 for v in v_lissee]
    ax1.plot(t_lissee, 'g', label="Filtrée")
    ax2.hist(t_lissee, label="T° lissée")
    ax1.legend()
    ax1.set_title("Température")
    ax2.set_title("Histogrammes d'erreur")
    ax2.legend()

    plt.show()


def rmse(v, t):
    # on renvoie la racine du quotient entre [la somme des éléments d'une liste par compréhension créée à partir
    # de la formule donnée dans l'énoncé] et N ; on pose N = len(v) = len(t) car t est créée à partir de v
    # print(f'v[0] = {v[0]} \nt[0] = {t[0]} \ncalcul = {10 * v[0] - 10 - t[0]}')
    return np.sqrt(np.sum([(10 * v[i] - 10 - t[i]) ** 2 for i in range(1, len(v))]) / len(v))


if __name__ == "__main__":
    main()

