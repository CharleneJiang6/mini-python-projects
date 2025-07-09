from tkinter import *
from math import *

# Remarques sur les modifs à faire au niveau front-end
# touches à implémenter : virgule, parenthèse fermant, hist, clear
# frame HIST a bien placer
# zone affichage calcul à placer
# emplacements des touches à harmoniser

class Calculatrice(Tk):
    """Classe permettant de créer une calculatrice."""

    def __init__(self):
        super().__init__()
        self.title('Calculatrice')

        # Taille de la fenêtre
        self.geometry('400x600')
        self.centrer_fenetre()

        self.output = StringVar() # la chaine de caractères du calcul
        self.math_formula = StringVar() # la chaine de calcul à évaluer, permettant à python de faire le calcul
        self.liste_historique : list[str] = []
        self.boutons_historiques : list[Button] = []
        self.label_erreur=StringVar()

        # Définition d'un frame principal "container"
        self.container = Frame(self).grid(row=0, column=0)

        # Définition d'un frame pour l'historique
        self.frame_historique = Frame(self).grid(row=0, column=1) 

        # Définition de la zone d'affichage
        self.entete = Frame(self.container).grid(row=0, column=0)
        Label(self.entete, textvariable=self.output).grid(row=3, column=3)
        Label(self.entete, textvariable=self.label_erreur).grid(row=2, column=3)


        # Définition d'une zone pour le clavier
        self.clavier = Frame(self.container)
        self.clavier.grid(row=1, column=0)
        charlist = ["1", "2", "3", "+", "C", "4", "5", "6", "-", "cos", "7", "8", "9", "*", "sin", "0", "𝜋", "𝜋²", "%", "tan"]
        
        # Création des boutons
        for row in range(3, 7):
            for column in range(1, 6):
                # pour chaque bouton, on lui donne comme texte un index unique de la charlist
                # on utilise une expression lambda pour pouvoir passer un paramètre à notre méthode click_button
                # lambda ne prend aucun argument donc notre paramètre "command" du bouton est content
                Button(self.clavier, text=charlist[5 * (row - 3) + column - 1], height=3, width=5,
                          command=lambda value=charlist[5 * (row - 3) + column - 1]: self.click_button(value)).grid(
                    row=row,
                    column=column,
                    sticky="nsew")
        # on ajoute ensuite les boutons séparés
        (Button(self.clavier, text="√𝑥", height=3, width=5, command=lambda : self.click_button("√"))
         .grid(row=8, column=4, sticky="nsew"))
        (Button(self.clavier, text="=", height=3, width=5, command=self.resultat)
         .grid(row=8, column=5, sticky="nsew"))
        (Button(self.clavier, text=")", height=3, width=5, command=lambda : self.click_button(")"))
         .grid(row=9, column=4, sticky="nsew"))
        (Button(self.clavier, text="/", height=3, width=5, command=lambda : self.click_button("/"))
         .grid(row=9, column=5, sticky="nsew"))
        (Button(self.clavier, text=".", height=3, width=5, command=lambda : self.click_button("."))
         .grid(row=9, column=3, sticky="nsew"))

        (Button(self.clavier, text="Clear", height=3, width=5, command = self.clear).grid(row=9, column=2, sticky="nsew"))
        (Button(self.clavier, text="hist", height=3, width=5, command=self.clic_historique)).grid(row=9, column=1, sticky="nsew")

        self.clavier.grid_rowconfigure(0, minsize=20)
        self.clavier.grid_rowconfigure(2, minsize=20)




    def click_button(self, button_value:str):
        '''Evaluer la valeur afficher sur par un bouton afin de l'afficher sur l'interface'''
        
        # update de l'expression mathématique 
        self.label_erreur.set('')
        correspondance={'sin':'sin(','cos':'cos(','tan':'tan(',"√":'sqrt(',"𝜋":'pi', "𝜋²":'pi**2', "%":'/100'}
        if button_value in correspondance:
            self.math_formula.set(self.math_formula.get()+correspondance[button_value])
            
        else: #pr les autres boutons numériques, pas de transformations à faire
            self.math_formula.set(self.math_formula.get()+button_value)

        # update de l'expression lisible par l'utilisateur
        if button_value in  ['sin','cos','tan',"√"]:
            self.output.set(self.output.get()+button_value+'(')
        else:
            self.output.set(self.output.get()+button_value)
        

    def clear(self):
        '''Efface la zone d'affichage, l'expression mathématique et le label pour les erreurs éventuelles.'''
        self.output.set('')
        self.math_formula.set('')
        self.label_erreur.set('')


    def resultat(self):
        '''Calcule et renvoie le résultat final du calcul.'''

        # Le clic sur le bouton '=' ne fonctionne que si un calcul a été saisi.
        if self.math_formula.get() != '':

            try:
                result=eval(self.math_formula.get())
                print(result)
                            
            except Exception as error:

                dico_errors={
                ZeroDivisionError : '\nERROR: division par 0',
                SyntaxError : '\nERROR: syntaxte incorrecte',
                ValueError : '\nERROR: valeur incorrecte'
            }
                if type(error) in dico_errors:
                    self.clear()
                    self.label_erreur.set(dico_errors[type(error)])
                else:
                    self.label_erreur.set('\nVeuillez retenter le calcul.')

            # OU BIEN : gérer les exceptions individuellement
            # except ZeroDivisionError:
            #     self.clear()
            #     self.label_erreur.set('\nERROR: division par 0')
            # except SyntaxError:
            #     self.clear()
            #     self.label_erreur.set('\nERROR: syntaxte incorrecte')
            # except ValueError:
            #     self.clear()
            #     self.label_erreur.set('\nERROR: valeur incorrecte')
    
            else:
                self.output.set(self.output.get()+'='+str(result))
                self.liste_historique.append(self.output.get())
                
                # Mettre à jour automatiquement l'historique
                self.historique()
            
 
    def historique(self):
        '''Affiche les 5 derniers résultats de l'historique des calculs'''

        self.label_erreur.set('')

        # Supression des précédents calculs dans l'historique
        self.boutons_historique = [boutons.destroy() for boutons in self.boutons_historiques]

        self.boutons_historiques = [
            Button(
                self.frame_historique,
                text=resultat,
                relief=FLAT,
                command=lambda resultat=resultat: (self.output.set(f'{resultat}'))
            )
            for resultat in self.liste_historique[-5:]
        ]
        for button in self.boutons_historiques:
            button.grid()
    
    
    def clic_historique(self):
        '''
        Le clic sur le bouton HIST permet de changer la taille de la fenêtre
        pour montrer ou cacher l'historique.
        '''
        if self.winfo_width() == 400: 
            self.geometry("800x600") 
        else:
            self.geometry("400x600")
        self.centrer_fenetre()
    

    def centrer_fenetre(self):
        '''Centre la fenêtre au centre de l'écran'''

        # s'assure que les dimensions de la fenêtre sont à jour avant de calculer la nouvelle position
        self.update_idletasks()

        largeur = self.winfo_width()
        hauteur = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largeur // 2)
        y = (self.winfo_screenheight() // 2) - (hauteur // 2)
        self.geometry('{}x{}+{}+{}'.format(largeur, hauteur, x, y))


def main():
    fenetre = Calculatrice()
    fenetre.mainloop()


if __name__=='__main__':
    main()