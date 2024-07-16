#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pdfkit
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calcul_de_chaleur(T_bet, T_cal, T_ctl, t, alpha, C_tot):
    theta = T_bet - T_ctl
    q_t = (C_tot / alpha) * (T_bet - T_cal)
    return theta, q_t

class AppInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Essai de Dégagement de Chaleur du Béton")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Frames
        input_frame = ttk.Frame(self, padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True)

        result_frame = ttk.Frame(self, padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Inputs
        ttk.Label(input_frame, text="Températures béton (séparées par des virgules):").grid(row=0, column=0, sticky=tk.W)
        self.T_bet_entry = ttk.Entry(input_frame, width=50)
        self.T_bet_entry.grid(row=0, column=1)

        ttk.Label(input_frame, text="Températures calorimètre:").grid(row=1, column=0, sticky=tk.W)
        self.T_cal_entry = ttk.Entry(input_frame, width=50)
        self.T_cal_entry.grid(row=1, column=1)

        ttk.Label(input_frame, text="Températures témoin:").grid(row=2, column=0, sticky=tk.W)
        self.T_ctl_entry = ttk.Entry(input_frame, width=50)
        self.T_ctl_entry.grid(row=2, column=1)

        ttk.Label(input_frame, text="Temps (heures):").grid(row=3, column=0, sticky=tk.W)
        self.t_entry = ttk.Entry(input_frame, width=50)
        self.t_entry.grid(row=3, column=1)

        ttk.Label(input_frame, text="Coefficient de déperdition thermique:").grid(row=4, column=0, sticky=tk.W)
        self.alpha_entry = ttk.Entry(input_frame)
        self.alpha_entry.grid(row=4, column=1)

        ttk.Label(input_frame, text="Capacité thermique totale:").grid(row=5, column=0, sticky=tk.W)
        self.C_tot_entry = ttk.Entry(input_frame)
        self.C_tot_entry.grid(row=5, column=1)

        # Bouton de calcul
        ttk.Button(input_frame, text="Calculer", command=self.calculate).grid(row=6, column=0, columnspan=2, pady=10)

        # Zone de résultats
        self.result_text = tk.Text(result_frame, height=10, width=80)
        self.result_text.pack()

        # Zone pour le graphique
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas.get_tk_widget().pack()

    def calculate(self):
        try:
            T_bet = np.array([float(x.strip()) for x in self.T_bet_entry.get().split(',')])
            T_cal = np.array([float(x.strip()) for x in self.T_cal_entry.get().split(',')])
            T_ctl = np.array([float(x.strip()) for x in self.T_ctl_entry.get().split(',')])
            t = np.array([float(x.strip()) for x in self.t_entry.get().split(',')])
            alpha = float(self.alpha_entry.get())
            C_tot = float(self.C_tot_entry.get())

            theta, q_t = calcul_de_chaleur(T_bet, T_cal, T_ctl, t, alpha, C_tot)

            # Affichage des résultats
            result_str = f"Résultats:\nTheta: {theta.tolist()}\nDégagement de chaleur: {q_t.tolist()}"
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, result_str)

            # Mise à jour du graphique
            self.ax.clear()
            self.ax.plot(t, q_t, label="Dégagement de chaleur")
            self.ax.set_xlabel("Temps (heures)")
            self.ax.set_ylabel("Dégagement de chaleur (Joules)")
            self.ax.set_title("Dégagement de chaleur en fonction du temps")
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()

            # Sauvegarde du graphique
            plt.savefig('resultat.png')

            # Génération du PDF
            self.generate_pdf(alpha, C_tot, t, q_t)

            messagebox.showinfo("Succès", "Calculs effectués et rapport PDF généré avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def generate_pdf(self, alpha, C_tot, t, q_t):
        html_str = f"""
        <html>
        <head><title>Rapport d'Essai</title></head>
        <body>
            <h1>Rapport d'Essai de Dégagement de Chaleur</h1>
            <h2>Paramètres de l'essai</h2>
            <p>Coefficient de déperdition thermique : {alpha}</p>
            <p>Capacité thermique totale : {C_tot}</p>
            <h2>Résultats</h2>
            <p>Temps (heures) : {t.tolist()}</p>
            <p>Dégagement de chaleur (Joules) : {q_t.tolist()}</p>
            <img src="resultat.png" alt="Graphique des résultats">
        </body>
        </html>
        """
        with open("rapport.html", "w") as file:
            file.write(html_str)
        pdfkit.from_file("rapport.html", "rapport.pdf")

if __name__ == "__main__":
    app = AppInterface()
    app.mainloop()