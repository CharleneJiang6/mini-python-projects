import tkinter as tk


class Calculatrice(tk.Tk):
    """Classe permettant de créer une calculatrice."""

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Calculatrice")
        self.bg = "black"

        self.output = tk.StringVar()
        self.history_status = False
        self.history_list: list[str] = []
        self.history_memory = ""
        self.math_formula = tk.StringVar()
        self.label_erreur = tk.StringVar()
        self.has_result = False

        # frame principal contenant tous les éléments
        self.container = tk.Frame(self)
        self.container.pack()

        # frame de l'entête
        self.entete = tk.Frame(self.container)
        self.entete.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

        custom_font = ("Courier New", 10)
        # on place l'output dans l'entête
        # on déclare le label séparément du pack pour pouvoir le rappeler et modifier sa configuration
        self.affichage = (tk.Label(self.entete,
                                   textvariable=self.output,
                                   bg='white',
                                   relief="sunken",
                                   borderwidth=3,
                                   font=custom_font,
                                   anchor='e',
                                   height=2,
                                   fg='black'))
        self.affichage.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.entete, textvariable=self.label_erreur, fg="red").pack(side="right")
        tk.Button(self.entete, text="Historique", command=self.toggle_history).pack(side='left')

        # bouton pour recentrer et réajuster la fenêtre
        tk.Button(self.entete, text="⨀", command=self.centrer_fenetre).pack(side="left")

        # frame du clavier
        self.clavier = tk.Frame(self.container)
        self.clavier.pack()
        charlist = ["1", "2", "3", "+", "C",
                    "4", "5", "6", "-", "cos",
                    "7", "8", "9", "×", "sin",
                    "𝜋", "0", "𝜋²", "/", "tan",
                    "(", ")", ".", "√", "="]

        for row in range(0, 5):
            for column in range(0, 5):
                # pour chaque bouton, on lui donne comme texte un élément unique de la charlist
                # on utilise une expression lambda pour pouvoir passer un paramètre à notre méthode click_button
                # lambda permet d'éxecuter la méthode avec l'argument désiré au moment du clic
                (tk.Button(self.clavier,
                           text=charlist[5 * row + column],
                           height=3, width=8, relief="raised",
                           command=lambda value=charlist[5 * row + column]: self.click_button(value))
                 .grid(row=row, column=column, sticky="nsew"))

        # une fois que tous nos widgets sont placés, on redimensionne la page pour tout fit
        self.centrer_fenetre()

    def click_button(self, button_value: str):
        """Évalue la valeur affichée par un bouton afin de l'afficher sur l'interface"""

        # efface l'affichage si la dernière opération a donné un résultat dans l'output
        if self.has_result:
            self.clear()
            self.has_result = False

        # update de l'expression mathématique
        self.label_erreur.set('')
        correspondance = {'sin': 'math.sin(',
                          'cos': 'math.cos(',
                          'tan': 'math.tan(',
                          "√": 'math.sqrt(',
                          "𝜋": 'math.pi',
                          "𝜋²": 'math.pi**2',
                          '×': '*',
                          '=': ''}
        if button_value in correspondance:
            # si on a sin, cos, tan, √ ou 𝜋 précédé par quelque chose qui n'est pas ×, on supppose
            # une multiplication implicite et on ajoute un * entre les 2
            if (button_value != '×' and button_value != '=' and len(self.math_formula.get()) > 0
                    and self.math_formula.get()[-1:] != '*' and self.math_formula.get()[-1:] != '('):
                self.math_formula.set(self.math_formula.get() + "*" + correspondance[button_value])
            else:
                self.math_formula.set(self.math_formula.get() + correspondance[button_value])
        else:  # pr les autres boutons numériques, pas de transformations à faire
            self.math_formula.set(self.math_formula.get() + button_value)

        # update de l'expression lisible par l'utilisateur
        if button_value in ['sin', 'cos', 'tan', "√"]:
            self.output.set(self.output.get() + button_value + '(')
        elif button_value == "C":
            self.clear()
        elif button_value == "=":
            self.resultat()
        else:
            self.output.set(self.output.get() + button_value)

    def clear(self):
        """Efface la zone d'affichage, l'expression mathématique et le label pour les erreurs éventuelles."""
        self.output.set('')
        self.math_formula.set('')
        self.label_erreur.set('')

    def resultat(self):
        """Calcule et renvoie le résultat final du calcul."""

        # Le clic sur le bouton '=' ne fonctionne que si un calcul a été saisi.
        if self.math_formula.get() != '':

            try:
                result = eval(self.math_formula.get())

            except SyntaxError:
                # en cas d'erreur de syntaxe on essaye d'abord d'ajouter une parenthèse pour voir si le pb se résout
                try:
                    result = eval(self.math_formula.get() + ")")

                except TypeError:
                    self.clear()
                    self.label_erreur.set('ERREUR : Un argument était attendu.')

                except ValueError:
                    self.clear()
                    self.label_erreur.set('ERREUR : Valeur incorrecte.')

                except SyntaxError:
                    self.clear()
                    self.label_erreur.set('ERREUR : Syntaxe incorrecte.')

                except ZeroDivisionError:
                    self.clear()
                    self.label_erreur.set('ERREUR : Division par 0 impossible.')

                else:
                    self.label_erreur.set('INFO : Parenthèse implicite ajoutée')
                    self.output.set(self.output.get() + ')=' + str(result))
                    self.history_list.append(self.output.get())
                    self.has_result = True

            except ZeroDivisionError:
                self.clear()
                self.label_erreur.set('ERREUR : Division par 0 impossible.')

            except ValueError:
                self.clear()
                self.label_erreur.set('ERREUR : Valeur incorrecte.')

            # on ne traite pas les autres exceptions
            except Exception:
                self.clear()
                self.label_erreur.set('Veuillez retenter le calcul.')

            # OU BIEN : gérer les exceptions ensemble
            # except Exception as error:
            #    dico_errors = {
            #        ZeroDivisionError: 'ERREUR : Division par 0 impossible.',
            #        SyntaxError: 'ERREUR : Syntaxe incorrecte.',
            #        ValueError: 'ERREUR : Valeur incorrecte.'
            #    }
            #    if type(error) in dico_errors:
            #        self.clear()
            #        self.label_erreur.set(dico_errors[type(error)])
            #    else:
            #        self.label_erreur.set('Veuillez retenter le calcul.')

            else:
                self.output.set(self.output.get() + '=' + str(result))
                self.history_list.append(self.output.get())
                self.has_result = True

        else:
            self.label_erreur.set("Veuillez entrer un calcul.")

    def toggle_history(self):
        """
        Le clic sur le bouton Historique permet d'afficher l'historique ou de le cacher.
        """
        self.history_status = not self.history_status

        if self.history_status:
            largeur = self.affichage.winfo_width()
            self.clavier.pack_forget()
            self.history_memory = self.affichage.cget("text")

            # affiche les 10 derniers résultats dans l'historique
            self.output.set("Historique:\n" + '\n'.join(self.history_list[-10:]))
            self.affichage.config(height=11)
        else:
            self.clavier.pack()
            self.output.set(self.history_memory)
            self.affichage.config(height=2)

    def centrer_fenetre(self):
        """Centre la fenêtre au centre de l'écran"""

        # on empêche l'utilisateur de centrer en étant dans l'historique car cela va modifier la taille de la fenêtre
        if not self.history_status:
            # s'assure que les dimensions de la fenêtre sont à jour avant de calculer la nouvelle position
            self.update()

            largeur = self.container.winfo_width()
            hauteur = self.container.winfo_height()
            x = (self.winfo_screenwidth() // 2) - (largeur // 2)
            y = (self.winfo_screenheight() // 2) - (hauteur // 2)
            self.geometry('{}x{}+{}+{}'.format(largeur, hauteur, x, y))


def main():
    fenetre = Calculatrice()
    fenetre.mainloop()


if __name__ == '__main__':
    main()
