import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

def main():

    # Q1
    image = plt.imread('citroen.jpg')
    # plt.imshow(image)
    # plt.show()

    # Q2
    # rouge_prime = image[:,:,0] / 255
    # vert_prime = image[:,:,1] / 255
    # bleu_prime = image[:,:,2] / 255

    # équivaut à diviser toute la matrice 3D par 255
    image2 = image.copy() / 255  #on fait une copie pour ne pas modifier l'original

    # recherche de la valeur minimal sur la profondeur, cad, pour 1 pixel, je regarde si
    # le min (resp. max) est sur le canal rouge, vert, ou bleu ? 
    c_min = image2.min(axis=2) 
    c_max = image2.max(axis=2)
    delta = c_max - c_min
    # print(delta.shape, '\n', delta)

    # on veut l'indice de la valeur max : elle est située sur quel plan ?
    # c_max_indice = image2.argmax(axis=2) # retourne une matrice
    # print(c_max_indice)


    matrices_bool = []
    for plan in range(3):
        # mat_bool=c_max_indice.copy()
        # mat_bool[c_max_indice==plan]=True
        # mat_bool[c_max_indice!=plan]=False

        mat_bool = (image2[:, :, plan] == c_max)  
        #pour chaque pixel de l'image à la profondeur [plan], est-il égal au pixel à la mm pos dans c_max

        # print(mat_bool)
        matrices_bool.append(mat_bool)
    # print(matrices_bool[1])


    # pour ignorer les divisions possibles par 0, dans les divisions par delta
    np.seterr(divide='ignore', invalid='ignore')

    # CALCUL DE H avec np.select
    # par exemple pour H_rouge, on récupère le reste de la division de X = (image2[:,:,1]-image2[:,:,2])/delta par 6
    # X résulte d'opérations matricielles : on fait la différence du canal vert par le canal bleu, terme à terme
    # puis chaque terme est divisé par delta
    # enfin chaque terme est multiplié par 1/6
    # au final on obtient une matrice 
    H_rouge = (1/6)*np.mod((image2[:,:,1]-image2[:,:,2])/delta,6)
    H_vert = (1/6)*(((image2[:,:,2]-image2[:,:,0])/delta)+2)
    H_bleu = (1/6)*(((image2[:,:,0]-image2[:,:,1])/delta)+4)
    # print(H_bleu.shape)

    choiceliste = [H_rouge, H_vert, H_bleu]


    # on parcourt les n matrices bool dans matrices_bool et à chaque fois on regarde l'élément à la position (i,j)
    # Si cet élément vaut True et s'il provient de la k-ième matrice (k<=n)
    # alors on va chercher dans choicelist la k-ième matrice, l'élément à la position (i,j)
    # Ainsi, cet élément constitue l'élément à la position (i,j) de la matrice finale H
    # Si pour une même position parmi les n matrices bool, plusieurs True sont rencontrés,
    # alors c'est le 1e True rencontré qui prime
    # Si aucun True n'est rencontré, la valeur par défaut qu'on mettra dans notre matrice H
    # à la position (i,j) sera 0
    H = np.select(matrices_bool, choiceliste, default=0)  #retourne mat 2D
    # print(H.shape)


    # soit p un pixel dans c_max à la position m. 
    # si p!=0, on va chercher la valeur dans la matrice (delta/c_max) à la position m
    # si p == 0, on prend 0 comme valeur par défaut
    S = np.select([c_max!=0],[delta/c_max],default=0)   #retourne mat 2D
    # print(S.shape)   

    # copie de c_max pour ne pas modifier l'orignal
    V = c_max.copy()
    # print(V.shape)

    # on concatène les 3 matrices H, S et V sur la profondeur. résultat = image en HSV
    mat_hsv = np.dstack((H,S,V))
    # print(mat_hsv.shape)


    # Verif
    hsv_converted_to_rgb = hsv_to_rgb(mat_hsv)
    # print(hsv_converted_to_rgb.shape)
    # plt.imshow(hsv_converted_to_rgb)
    # plt.show()   # yes on obtient l'image originale !



    # Q3

    # affichage des 3 plans individuels
    # definition d'une figure avec 1 ligne et 3 colonne

    # fig, axes = plt.subplots(1, 3)
    # for ax, channel in zip(axes, (H, S, V)):
    #     im = ax.imshow(channel, vmin=0, vmax=1)
    #     fig.colorbar(im, ax=ax)
    # plt.show()

    # OU bien
    # for plan in [H,S,V]:
    #     plt.imshow(plan)
    #     plt.colorbar()
    #     plt.show()


    # RECHERCHE des paliers pour faire ressortir la carrosserie

    mat_hsv_copy = mat_hsv.copy()

    # d'après les valeurs estimées grâce aux colorbars
    # les conditions que la carrosserie doit vérifier sont surtout :
    # la teinte H qui se trouve autour de 0.5
    # et la saturation S proche de 1 (et qq pixel autour de 0.4 présentant de l'ombre)
    mask = (
        (mat_hsv_copy[:,:,0]>=0.5) & 
        (mat_hsv_copy[:,:,0]<=0.6) & 
        ((mat_hsv_copy[:,:,1] >= 0.9) | ((mat_hsv_copy[:,:,1] >= 0.4) & (mat_hsv_copy[:,:,1] >= 0.4)))
        )
    # (np.round(mat_hsv_copy[:,:,1], decimals=1) == 0.4)

    # si la matrice mat_hsv_copy vérifie toute les conditions, alors, on change sa couleur en rouge
    mat_hsv_copy[mask] = 1


    plt.imshow(hsv_to_rgb(mat_hsv_copy))
    plt.show()



if __name__ == "__main__":
    main()


# ====================================================================
# brouillon : 1e TEST pour changer la couleur :
# # le ciel change de couleur ....

# # pour arrondir les valeurs à un décimal après la virgule
# # print(np.round(1.598,decimals=1))

# mask_h = np.round(mat_hsv[:,:,0].copy(),decimals=1)
# mask_h[(mask_h>=0.5) & (mask_h<=0.6)] = 0 #fixe a la val max
# # print(mask_h.shape)

# mask_s = np.round(mat_hsv[:,:,1].copy(),decimals=1)
# mask_s[(mask_s>=0.4) & (mask_s<=0.6)] = 1 #fixe a la val max
# mask_s[mask_s==1.0] = 1
# # print(mask_s.shape)


# mask_v = np.round(mat_hsv[:,:,2].copy(),decimals=1)
# mask_v[(mask_v>=0.4) & (mask_v<=0.8)] = 1 #fixe a la val max
# # print(mask_v.shape)


# mat_hsv_carroserie_modifiee = np.dstack((mask_h,mask_s, mask_v))
# # print(mat_hsv_carroserie_modifiee.shape)

# mat_hsv_convert_to_rgb = hsv_to_rgb(mat_hsv_carroserie_modifiee)
# # plt.imshow(mat_hsv_convert_to_rgb)
# # plt.show()