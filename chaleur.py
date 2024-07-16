import matplotlib.pyplot as plt
import numpy as np
import pdfkit

def calcul_de_chaleur(T_bet, T_cal, T_ctl, t, alpha, C_tot):
    theta = T_bet - T_ctl
    q_t = (C_tot / alpha) * (T_bet - T_cal)
    return theta, q_t

def main():
    print("Essai de Dégagement de Chaleur du Béton")

    # Saisie des données
    T_bet = np.array([float(x) for x in input("Températures béton (séparées par des espaces): ").split()])
    T_cal = np.array([float(x) for x in input("Températures calorimètre: ").split()])
    T_ctl = np.array([float(x) for x in input("Températures témoin: ").split()])
    t = np.array([float(x) for x in input("Temps (heures): ").split()])
    alpha = float(input("Coefficient de déperdition thermique: "))
    C_tot = float(input("Capacité thermique totale: "))

    # Calcul
    theta, q_t = calcul_de_chaleur(T_bet, T_cal, T_ctl, t, alpha, C_tot)

    # Affichage des résultats
    print("\nRésultats:")
    print(f"Theta: {theta.tolist()}")
    print(f"Dégagement de chaleur: {q_t.tolist()}")

    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(t, q_t, label="Dégagement de chaleur")
    plt.xlabel("Temps (heures)")
    plt.ylabel("Dégagement de chaleur (Joules)")
    plt.title("Dégagement de chaleur en fonction du temps")
    plt.legend()
    plt.grid(True)
    plt.savefig('resultat.png')
    plt.close()

    # Génération du PDF
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

    print("\nLe rapport PDF a été généré avec succès.")

if __name__ == "__main__":
    main()