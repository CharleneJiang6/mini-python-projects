import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb


def rgb_to_hsv(image: str) -> np.ndarray:
    """
    Convertit une image RGB en format HSV.
    :param image: array d'une image en RGB (lue avec plt.imread par exemple)
    :return: array de l'image en HSV
    """
    image_copy = image.copy() / 255

    # recherche de la valeur minimal sur la profondeur, ie, pour 1 pixel, je regarde si
    # le min (resp. max) est-il sur le canal rouge, vert, ou bleu ?
    c_min = image_copy.min(axis=2)
    c_max = image_copy.max(axis=2)
    # V est égal à l'array c_max donc pas la peine de créer 2 variables différentes
    v = image_copy.max(axis=2)
    delta = c_max - c_min

    # pour ignorer les divisions potentielles par 0, notamment dans les divisions par delta
    np.seterr(divide='ignore', invalid='ignore')

    # on crée une nouvelle matrice qui sera de même taille que l'image, mais contenant True pour chaque index où l'on
    # trouve un c_max, False sinon, en comparant pour chaque plan (r, g, b) si la valeur est égale à celle de c_max (=V)
    c_max_bool = [(image_copy[:, :, plan] == v) for plan in range(3)]

    conditions = [c_max_bool[0], c_max_bool[1], c_max_bool[2]]
    # on crée 3 matrices déjà calculées avec les valeurs de H dans chaque cas
    # on sélectionnera ensuite la valeur d'une seule de ces matrices pour chaque pixel en fonction de la valeur de c_max

    # ensuite, pour h_rouge, on récupère le reste de la division de X = (image2[:,:,1]-image2[:,:,2])/delta par 6
    # X résulte d'opérations matricielles : on fait la différence du canal vert par le canal bleu, terme à terme
    # puis chaque terme est divisé par delta
    # enfin chaque terme est multiplié par 1/6
    # au final on obtient une matrice 
    h_rouge = (1 / 6) * np.mod((image_copy[:, :, 1] - image_copy[:, :, 2]) / delta, 6)
    h_vert = (1 / 6) * (((image_copy[:, :, 2] - image_copy[:, :, 0]) / delta) + 2)
    h_bleu = (1 / 6) * (((image_copy[:, :, 0] - image_copy[:, :, 1]) / delta) + 4)
    choiceliste = [h_rouge, h_vert, h_bleu]
    h = np.select(conditions, choiceliste, default=0)
    # on parcourt les n matrices bool dans conditions et à chaque fois on regarde l'élément à la position (i,j)
    # Si cet élément vaut True et s'il provient de la k-ième matrice (k<=n)
    # alors on va chercher dans choiceliste la k-ième matrice, l'élément à la position (i,j)
    # Ainsi, cet élément constitue l'élément à la position (i,j) de la matrice finale H
    # Si pour une même position parmi les n matrices booléens, plusieurs True sont rencontrés,
    # alors c'est le 1e True rencontré qui prime
    # Si aucun True n'est rencontré, la valeur par défaut qu'on mettra dans notre matrice H
    # à la position (i,j) sera 0

    # soit p un pixel dans c_max à la position m.
    # si p!=0, on va chercher la valeur dans la matrice (delta/c_max) à la position m
    # si p == 0, on prend 0 comme valeur par défaut
    s = np.select([c_max != 0], [delta / c_max], 0)

    # on concatène les 3 matrices H, S et V sur la profondeur. résultat = image en HSV
    return np.dstack((h, s, v))


def afficher_canaux_hsv(image: str) -> None:
    """
    Affiche des images des canaux HSV séparés.
    :param image: image HSV
    :return:
    """
    for plan in range(3):  # car 3 plans H,S,V
        plt.imshow(image[:, :, plan])
        plt.colorbar()
        plt.show()

    # ou bien :
    # plt.imshow(image[:, :, 0])  # H
    # plt.colorbar()
    # plt.show()
    # plt.imshow(image[:, :, 1])  # S
    # plt.colorbar()
    # plt.show()
    # plt.imshow(image[:, :, 2])  # V
    # plt.colorbar()
    # plt.show()


def main():
    image = plt.imread('citroen.jpg')
    plt.imshow(image)
    plt.show()

    image_hsv = rgb_to_hsv(image)

    # verif : on reconvertit notre image HSV en RGB puis on l'affiche
    # hsv_converted_to_rgb = hsv_to_rgb(image_hsv)
    # print(hsv_converted_to_rgb.shape)
    # plt.imshow(hsv_converted_to_rgb)
    # plt.show()   on obtient bien l'image originale

    # affichage des 3 plans individuels
    afficher_canaux_hsv(image_hsv)
    # à l'aide d'une pipette HSV on estime ~ H = 200/360 S = 95--100/100 V = 60--80/100

    image_hsv_copy = image_hsv.copy()
    # d'après les valeurs estimées grâce aux colorbars
    # les conditions que la carrosserie doit vérifier sont surtout :
    # la teinte H qui se trouve autour de 0.5
    # et la saturation S proche de 1 (et qq pixels autour de 0.4 présentant de l'ombre)
    mask = (
            (image_hsv_copy[:, :, 0] >= 0.5) &
            (image_hsv_copy[:, :, 0] <= 0.6) &
            ((image_hsv_copy[:, :, 1] >= 0.9) | ((image_hsv_copy[:, :, 1] >= 0.3) & (image_hsv_copy[:, :, 0] >= 0.4))) &
            (image_hsv_copy[:, :, 2] >= 0.4)
    )
    # on a ainsi défini des conditions sur le canal 0, puis le canal 1. La condition sur le canal 2 est optionnel mais permet de s'assurer
    # du bon domaine de définition des pixels à retoucher.
    # à la 3e ligne du mask, le "OU" permet de prendre à la fois les zones où la carrosserie présente une grande saturation, et les zones ombrées

    # si la matrice image_hsv_copy vérifie toutes les conditions, alors, on change sa couleur en rouge
    image_hsv_copy[mask] = 1
    # on fait apparaître les ombres en appliquant la saturation (S) et valeur (V) présentes sur l'image de départ
    image_hsv_copy[:, :, 2] = image_hsv[:, :, 2]
    image_hsv_copy[:, :, 1] = image_hsv[:, :, 1]

    plt.imshow(hsv_to_rgb(image_hsv_copy))
    plt.show()


if __name__ == '__main__':
    main()
