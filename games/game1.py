import random

def jeu_devinette():
    print("Bienvenue dans le jeu de devinette de nombre!")
    print("Je pense à un nombre entre 1 et 100. Pouvez-vous le deviner?")
    nombre_secret = random.randint(1, 100)
    tentatives = 0
    devine = 0
    while devine != nombre_secret:
        devine = input("Entrez votre supposition (ou 'q' pour quitter): ")
        if devine.lower() == 'q':
            print(f"Le nombre secret était {nombre_secret}. Au revoir!")
            return
        try:
            devine = int(devine)
        except ValueError:
            print("Veuillez entrer un nombre valide ou 'q' pour quitter.")
            continue
        tentatives += 1
        if devine < nombre_secret:
            print("Trop bas! Essayez encore.")
        elif devine > nombre_secret:
            print("Trop haut! Essayez encore.")
        else:
            print(f"Félicitations! Vous avez deviné le nombre en {tentatives} tentatives!")

jeu_devinette()
