from tkinter import *
from typing import Callable
from math import *


class Calculatrice(Tk):
    """Classe permettant de créer une calculatrice."""

    def __init__(self, hauteur=600, largeur=400):
        super().__init__()
        self.title("Calculatrice")
        self.pos_x = self.winfo_screenwidth() // 2 - largeur // 2
        self.pos_y = self.winfo_screenheight() // 2 - hauteur // 2
        self.geometry(f'{largeur}x{hauteur}+{self.pos_x}+{self.pos_y}')

        self.affichage = StringVar()

        self.historique = []

        # Définition de 2 zones séparées pour la calculette et l'historique
        calculette = Frame(self).grid(row=0, column=0)
        historique = Frame(self).grid(row=0, column=1)

        # Initialisation des composants de la calculette
        padding = {'padx': 5, 'pady': 5}
        Label(calculette, text="CALCULATRICE", height=3).grid(
            row=0, column=0, columnspan=5, sticky='nsew', **padding
        )
        Label(
            calculette, width=50, height=2, textvariable=self.affichage, bg='white', relief=SUNKEN, borderwidth=3).grid(
            row=1, column=0, columnspan=4, sticky='nsew', **padding
        )

        self.create_button(calculette, 'π', 'yellow', lambda: self.click_button(pi), 2, 0)
        self.create_button(calculette, 'π²', 'yellow', lambda: self.click_button(pi ** 2), 2, 1)
        self.create_button(calculette, '√x', 'yellow', lambda: self.click_button(sqrt), 2, 2)
        self.create_button(calculette, '(', 'yellow', lambda: self.click_button('('), 2, 3)
        self.create_button(calculette, ')', 'yellow', None, 2, 4)
        self.create_button(calculette, 'cos', 'yellow', None, 3, 0)
        self.create_button(calculette, '1', 'yellow', None, 3, 1)
        self.create_button(calculette, '2', 'yellow', None, 3, 2)
        self.create_button(calculette, '3', 'yellow', None, 3, 3)
        self.create_button(calculette, '+', 'yellow', None, 3, 4)

    def create_button(self, parent: Frame, text: str, bg: str, command: Callable,
                      line: int, colonne: int, column_span: int = 1, border_width: int = 3,
                      padx: int = 5, pady: int = 5, sticky: str = 'nsew', relief='raised', largeur=5):
        button = Button(self, parent, text=text, bg=bg, command=command, borderwidth=border_width, relief=relief,
                        width=largeur)
        button.grid(row=line, column=colonne, columnspan=column_span, padx=padx, pady=pady, sticky=sticky)

    def click_button(self):
        pass

    def historique(self):
        pass


def main():
    calculatrice = Calculatrice()
    calculatrice.mainloop()


if __name__ == '__main__':
    main()
