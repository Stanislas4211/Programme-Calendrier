import tkinter as tk
from tkinter import filedialog
import csv

def choisir_fichier():
    # Ouvre une boîte de dialogue pour sélectionner un fichier .ics
    chemin_fichier = filedialog.askopenfilename(title="Sélectionner un fichier ICS", filetypes=[("Fichiers ICS", "*.ics")])
    
    # Affiche le chemin du fichier sélectionné
    if chemin_fichier:
        label_chemin.config(text=f"Fichier sélectionné : {chemin_fichier}")
        return chemin_fichier
    else:
        label_chemin.config(text="Aucun fichier sélectionné")
        return None

def quitter():
    # Ferme la fenêtre principale proprement
    fenetre.quit()

def lire_fichier_ics(fichier_ics):
    """Lecture du fichier ICS et extraction de son contenu"""
    with open(fichier_ics, 'r', encoding='utf-8') as file:
        contenu = file.read()
    return contenu

def extraire_donnees(contenu):
    """Extraction des informations clés depuis le fichier ICS"""
    evenement = {}

    for ligne in contenu.splitlines():
        if ligne.startswith("DTSTAMP"):
            evenement["DTSTAMP"] = ligne.split(":")[1]
        elif ligne.startswith("DTSTART"):
            evenement["DTSTART"] = ligne.split(":")[1]
        elif ligne.startswith("DTEND"):
            evenement["DTEND"] = ligne.split(":")[1]
        elif ligne.startswith("SUMMARY"):
            evenement["SUMMARY"] = ligne.split(":")[1]
        elif ligne.startswith("LOCATION"):
            evenement["LOCATION"] = ligne.split(":")[1]
        elif ligne.startswith("DESCRIPTION"):
            evenement["DESCRIPTION"] = ligne.split(":")[1]
    
    return evenement

def enregistrer_en_csv(donnees, nom_fichier):
    """Enregistre les données extraites dans un fichier CSV"""
    with open(nom_fichier, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["DTSTAMP", "DTSTART", "DTEND", "SUMMARY", "LOCATION", "DESCRIPTION"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerow(donnees)

def main():
    # Création de la fenêtre principale
    global fenetre, label_chemin
    fenetre = tk.Tk()
    fenetre.title("Sélectionner un fichier ICS")
    fenetre.geometry("400x200")

    # Ajout d'un bouton pour ouvrir le dialogue de sélection de fichier
    btn_choisir_fichier = tk.Button(fenetre, text="Choisir un fichier ICS", command=lambda: traiter_fichier())
    btn_choisir_fichier.pack(pady=20)

    # Label pour afficher le chemin du fichier
    label_chemin = tk.Label(fenetre, text="Aucun fichier sélectionné")
    label_chemin.pack(pady=20)

    # Ajout du bouton "Quitter"
    btn_quitter = tk.Button(fenetre, text="Quitter", command=quitter)
    btn_quitter.pack(pady=20)

    # Lancer l'interface graphique
    fenetre.mainloop()

def traiter_fichier():
    """Fonction pour traiter le fichier sélectionné et créer le fichier CSV"""
    fichier_ics = choisir_fichier()
    if fichier_ics:
        contenu = lire_fichier_ics(fichier_ics)
        donnees = extraire_donnees(contenu)
        enregistrer_en_csv(donnees, "evenement.csv")
        print("Fichier CSV créé avec succès !")

# Exécution de l'application
if __name__ == "__main__":
    main()
