#Exercice 1 - Calculatrice

#Import du module Tkinter
import tkinter.font
from tkinter import *
#Import du module functools pour placer un paramètre aux fonctions callback
from functools import partial
from math import *

#Classe pour la fenêtre de la calculatrice
class Calculatrice(Tk):
    #Initialisatin de la fenêtre
    def __init__(self, largeur = 400, hauteur = 600):
        #Initialisation de la classe mère
        super().__init__()

        #Ajout d'un titre à la fenêtre
        self.title('TP Calculatrice')

        #Definition de la taille de la fenêtre
        self.largeur_fenetre = largeur
        self.hauteur_fenetre = hauteur

        #Récupération des informations de l'écran de l'utilisateur
        self.largeur_ecran = self.winfo_screenwidth()
        self.hauteur_ecran = self.winfo_screenheight()

        #Calcul de la position à laquelle placer la fenêtre sur l'écran de l'utilisateur
        self.posx = self.largeur_ecran // 2 - self.largeur_fenetre // 2
        self.posy = self.hauteur_ecran // 2 - self.hauteur_fenetre // 2 - 50

        #Positionnement de la fenêtre sur l'écran de l'utilisateur
        self.geometry(f"{self.largeur_fenetre}x{self.hauteur_fenetre}+{self.posx}+{self.posy}")

        #Dictionnaires contenant les différents widgets
        self.labels = {}
        self.boutons = {}

        #Initialisation de la variable contenant l'expression mathématique du calcul souhaité par l'utilisateur
        self.expression = ''
        #Initialisation de la variable contenant l'expression mathématique du calcul souhaité par l'utilisateur
        self.affichage = ''

        #Initialisation d'un tableau avec l'ensemble des calculs réalisés
        self.list_historique = []

        #Ajout d'un label pour le titre de la calculatrice
        self.createLabel('titre', 'Calculatrice', 1, 0, 30, colonnespan = 5)

        #Ajout d'un label modélisant l'écran de la calculatrice
        self.createLabel('resultat', '', 2, 0, 30, border_largeur = 20, colonnespan= 5, bgcolor= 'white', \
                         alignement = E, relief=SUNKEN)

        #Ajout d'un label pour le titre de la partie historique
        self.createLabel('historique', 'Historique', 1, 5, 50, colonnespan = 5)


        #Ajout des boutons
        #Boutons pour les valeurs numériques
        self.createButton('1', 4, 1, commande = partial(self.modifier_calcul, '1', '1'), bgcolor = 'yellow')
        self.createButton('2', 4, 2, commande = partial(self.modifier_calcul, '2', '2'), bgcolor = 'yellow')
        self.createButton('3', 4, 3, commande = partial(self.modifier_calcul, '3', '3'), bgcolor = 'yellow')
        self.createButton('4', 5, 1, commande = partial(self.modifier_calcul, '4', '4'), bgcolor = 'yellow')
        self.createButton('5', 5, 2, commande = partial(self.modifier_calcul, '5', '5'), bgcolor = 'yellow')
        self.createButton('6', 5, 3, commande = partial(self.modifier_calcul, '6', '6'), bgcolor = 'yellow')
        self.createButton('7', 6, 1, commande = partial(self.modifier_calcul, '7', '7'), bgcolor = 'yellow')
        self.createButton('8', 6, 2, commande = partial(self.modifier_calcul, '8', '8'), bgcolor = 'yellow')
        self.createButton('9', 6, 3, commande = partial(self.modifier_calcul, '9', '9'), bgcolor = 'yellow')
        self.createButton('0', 7, 2, commande = partial(self.modifier_calcul, '0', '0'), bgcolor = 'yellow')
        #Boutons pour les opérateurs pour effectuer des calculs
        self.createButton('+', 4, 4, commande = partial(self.modifier_calcul, '+', '+'), bgcolor = 'skyblue')
        self.createButton('-', 5, 4, commande = partial(self.modifier_calcul, '-', '-'), bgcolor = 'skyblue')
        self.createButton('*', 6, 4, commande = partial(self.modifier_calcul, '*', '*'), bgcolor = 'skyblue')
        self.createButton('/', 7, 4, commande = partial(self.modifier_calcul, '/', '/'), bgcolor = 'skyblue')
        #Boutons pour les fonctions usuelles pour les calculs
        self.createButton('sin', 4, 0, commande = partial(self.modifier_calcul, 'sin(', 'sin('), bgcolor = 'purple')
        self.createButton('cos', 5, 0, commande = partial(self.modifier_calcul, 'cos(', 'cos('), bgcolor = 'purple')
        self.createButton('tan', 6, 0, commande = partial(self.modifier_calcul, 'tan(', 'tan('), bgcolor = 'purple')
        self.createButton('√x', 3, 0, commande = partial(self.modifier_calcul, '√(', 'sqrt('), bgcolor = 'purple')
        self.createButton('x²', 3, 1, commande = partial(self.modifier_calcul, '²', '**(2)'), bgcolor = 'purple')
        #Bouton pour la constante pi
        self.createButton('π', 3, 2, commande= partial(self.modifier_calcul, 'π', 'pi'), bgcolor = 'purple')
        #Boutons pour les parenthèses des calculs
        self.createButton('(', 3, 3, commande = partial(self.modifier_calcul, '(', '('), bgcolor = 'purple')
        self.createButton(')', 3, 4, commande = partial(self.modifier_calcul, ')', ')'), bgcolor = 'purple')

        #Bouton pour valider le calcul
        self.createButton('=', 7, 1, commande = self.valider_calcul, bgcolor = 'red')
        #Bouton pour les nombres à virgule (décimaux)
        self.createButton('.', 7, 3, commande = partial(self.modifier_calcul, '.', '.'), bgcolor = 'yellow')
        #Bouton pour effacer le calcul en cours
        self.createButton('clear', 7, 0, commande = self.effacer, bgcolor = 'green')


    #Fonctions nécéssaires
    def createLabel(self, nom, texte, ligne, colonne, largeur, border_largeur = 2, colonnespan = 1, \
                    alignement = CENTER, bgcolor = '#F0F0F0', relief = FLAT):
        """Création d'un label ayant un nom d'identification, un texte à afficher, une couleur d'arrière plan,
        se positionnant sur la grille à l'emplacement (ligne, colonne)"""
        #Création du label avec les différents attributs
        self.labels[nom] = Label(self, text = texte, bg = bgcolor, relief = relief, width = largeur, \
                                     borderwidth = border_largeur, anchor = alignement, font = tkinter.font.Font(family = "TkDefaultFont", size = 15))
        #Placement du label sur la grille de la fenêtre
        self.labels[nom].grid(row = ligne, column = colonne, columnspan = colonnespan, padx = 10, pady = 20)

    def createButton(self, nom_bouton, ligne, colonne, commande, bgcolor = '#F0F0F0', colonnespan = 1, relief = RAISED, sticky = N):
        """Création d'un bouton ayant un nom d'identification, un texte à afficher, une couleur d'arrière plan,
        se positionnant sur la grille à l'emplacement (ligne, colonne) et ayant une commande à activer"""
        #Création du bouton
        self.boutons[nom_bouton] = Button(self, text = nom_bouton, padx = 12, pady = 12, bg = bgcolor, borderwidth = 12, \
                                    relief = relief,command = commande)
        #Positionnement du bouton sur la grille
        self.boutons[nom_bouton].grid(row = ligne, column = colonne, pady = 5, columnspan = colonnespan,  sticky = sticky)

    def modifier_calcul(self, valeur_affichee, valeur_mathematique):
        "Mise à jour de l'affichage et de l'expression mathématique"
        #Modification de la chaine à afficher sur l'écran de la calculatrice
        self.affichage += valeur_affichee
        #Modification de l'expression mathématique avec la valeur choisie par l'utilisateur
        self.expression += valeur_mathematique
        #Mise à jour de l'affichage de la calculatrice
        self.labels['resultat'].config(text = self.affichage)

    def valider_calcul(self):
        "Calcul de l'expression mathématique demandée par l'utilisateur"
        #Evaluation de la valeur de l'expression mathématique pour obtenir le résultat si possible
        try:
            #Calcul du résultat
            self.resultat = str(eval(self.expression))
            #Mise à jour de l'affichage de la calculatrice
            self.labels['resultat'].config(text=f"{self.affichage}={self.resultat}")
            #Ajout du calcul à l'historique
            self.list_historique.insert(0, self.labels['resultat']['text'])
            #Initialisation de l'affichage et de l'expression avec la valeur du résultat pour le prochain calcul (pour avoir l'historique du résultat)
            self.affichage = self.resultat
            self.expression = self.resultat
            #Modification de l'historique
            self.historique()
        #S'il y a une erreur, on la capte et on l'affiche
        except ZeroDivisionError:
            #Affichage de l'erreur sur l'écran de la calculatrice
            self.labels['resultat'].config(text = "ERREUR DIVISION PAR 0")
            #Remise à 0 du texte l'expression mathématique et de l'affichage en vu du prochain calcul
            self.expression = ''
            self.affichage = ''
        except ValueError:
            # Affichage de l'erreur sur l'écran de la calculatrice
            self.labels['resultat'].config(text="ERREUR DE VALEUR")
            # Remise à 0 du texte l'expression mathématique et de l'affichage en vu du prochain calcul
            self.expression = ''
            self.affichage = ''
        except SyntaxError:
            # Affichage de l'erreur sur l'écran de la calculatrice
            self.labels['resultat'].config(text = "ERREUR DE SYNTAXE")
            # Remise à 0 du texte l'expression mathématique et de l'affichage en vu du prochain calcul
            self.expression = ''
            self.affichage = ''

    def effacer(self):
        "Efface le calcul en cours"
        #Effacage du texte à l'écran de la calculatrice et remise à vide de l'expression mathématique
        self.affichage = ''
        self.expression = ''
        #Suppression de l'affichage du résultat
        self.labels['resultat'].config(text=self.affichage)

    def historique(self):
        "Affiche l'historique des 5 derniers calculs"
        #Variable contenant le nombre de calculs à afficher dans la partie historique
        self.nb_calcul = 5
        #Parcours des derniers éléments de l'historique pour les afficher (uniquement en mode plein écran)
        for i, calcul in enumerate(self.list_historique[:self.nb_calcul]):
            #Extraction du résultat du calcul
            self.valeur = str(calcul.split('=')[1])
            #Création d'un bouton contenant le calcul
            self.createButton(f"{calcul}",  2 + i, 5, commande = partial(self.modifier_calcul, self.valeur, self.valeur), colonnespan = 5, relief = FLAT, sticky=NSEW)

#Programme principal
def main():
    #Création de la calculatrice
    calculatrice = Calculatrice()
    #Actualisation de la boucle principale
    calculatrice.mainloop()

if __name__ == "__main__":
    main()
