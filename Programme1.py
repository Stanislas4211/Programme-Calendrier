#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
from datetime import datetime

def lire_evenement_ics(fichier):
    """Lit un fichier .ics et extrait les infos principales d'un événement."""
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    uid = next(l[4:].strip() for l in lignes if l.startswith("UID:"))
    dtstart = next(l[8:].strip() for l in lignes if l.startswith("DTSTART:"))
    dtend = next(l[6:].strip() for l in lignes if l.startswith("DTEND:"))
    summary = next(l[8:].strip() for l in lignes if l.startswith("SUMMARY:"))
    location = next(l[9:].strip() for l in lignes if l.startswith("LOCATION:"))
    description = next(l[12:].strip() for l in lignes if l.startswith("DESCRIPTION:"))

    # Conversion des dates
    debut = datetime.strptime(dtstart, "%Y%m%dT%H%M%SZ")
    fin = datetime.strptime(dtend, "%Y%m%dT%H%M%SZ")
    date = debut.strftime("%d-%m-%Y")
    heure = debut.strftime("%H:%M")
    duree = fin - debut
    duree_str = f"{duree.seconds//3600:02d}:{(duree.seconds//60)%60:02d}"

    # Prof et groupe depuis DESCRIPTION (simplifié)
    desc_parts = description.split("\\n")
    groupe = desc_parts[1].strip() if len(desc_parts) > 1 else ""
    prof = desc_parts[2].strip() if len(desc_parts) > 2 else ""

    modalite = "CM"  # Exemple

    return [uid, date, heure, duree_str, modalite, summary, location, prof, groupe]


def choisir_fichier():
    chemin_fichier = filedialog.askopenfilename(title="Sélectionner un fichier .ics")
    if chemin_fichier:
        label_chemin.config(text=f"Fichier sélectionné : {chemin_fichier}")
        # Lecture et conversion
        valeurs = lire_evenement_ics(chemin_fichier)
        ecrire_csv(valeurs, "evenement.csv")
        label_resultat.config(text="Conversion terminée → evenement.csv")
    else:
        label_chemin.config(text="Aucun fichier sélectionné")


def ecrire_csv(valeurs, fichier_csv="evenement.csv"):
    entetes = ["uid","date","heure","duree","modalite","intitule","salle","prof","groupe"]
    with open(fichier_csv, "w", encoding="utf-8") as f:
        f.write(";".join(entetes) + "\n")
        f.write(";".join(valeurs) + "\n")


def quitter():
    fenetre.destroy()

fenetre = tk.Tk()
fenetre.title("Sélectionner un fichier ICS")
fenetre.geometry("400x250")

btn_choisir_fichier = tk.Button(fenetre, text="Choisir un fichier", command=choisir_fichier)
btn_choisir_fichier.pack(pady=10)

label_chemin = tk.Label(fenetre, text="Aucun fichier sélectionné")
label_chemin.pack(pady=10)

label_resultat = tk.Label(fenetre, text="")
label_resultat.pack(pady=10)

btn_quitter = tk.Button(fenetre, text="Quitter", command=quitter)
btn_quitter.pack(pady=10)

fenetre.mainloop()