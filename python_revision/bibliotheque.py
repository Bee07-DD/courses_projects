bibliotheque = []

livre_1 = {
    "titre": "1984",
    "auteur": "George Orwell",
    "annee": 1949,
    "disponible": True
}

livre_2 = {
    "titre": "Petit prince",
    "auteur": "Antoine de Saint-Exupéry",
    "annee": 1943,
    "disponible": True
}

livre_3 = {
    "titre": "Le Seigneur des Anneaux",
    "auteur": "J.R.R. Tolkien",
    "annee": 1954,
    "disponible": False
}

bibliotheque = [livre_1,livre_2,livre_3]

def afficher_livres (bibliotheque = None):
    if bibliotheque is None :
        bibliotheque = []
    for l in bibliotheque :
        for k,v in l.items() :
            print(f"{k}:{v}\n")

def rechercher_par_auteur(bibliotheque = None, auteur = ""):
    if  bibliotheque is None :
        bibliotheque = []
    results = []
    for l in bibliotheque :
        if l.get("auteur") == auteur :
            results.append((l.get("titre"),l.get("annee")))
            pass
    return results

# afficher_livres(bibliotheque)
# print(rechercher_par_auteur(bibliotheque, "George Orwell"))
def ajouter_livre(bibliotheque = None, titre = "", auteur = "", annee = 0):
    if bibliotheque is None :
        bibliotheque = []
    disc = {"titre": titre,
            "auteur": auteur,
            "annee": annee,
            "disponible": True
            }
    bibliotheque.append(disc)
       
def emprunter_livre (bibliotheque = None, titre = ""):
    if bibliotheque is None :
        bibliotheque = []
    for l in bibliotheque :
        if l.get("titre") == titre and l.get("disponible") :
            l["disponible"] = False
            return True
    return False
            

def livre_disponibles(bibliotheque = None):
    if bibliotheque is None :
        bibliotheque = []
    return [l.get("titre") for l in bibliotheque if l.get("disponible")]

def sauvegarder_bibliotheque (bibliotheque = None ,chemin = "bibliotheque.txt"):
    if bibliotheque is None :
        bibliotheque = []
    for l in bibliotheque :
        with open("biliotheque.txt","w") as f:
            f.write(f"{l['titre']};{l['auteur']};{l['annee']};{l['disponible']}\n")
            
def charger_bibliotheque (chemin = "bibliotheque.txt"):
    bibliotheque = []
    try:
        with open(chemin,"r") as f:
            for line in f:
                titre, auteur, annee, disponible = line.strip().split(";")
                livre = {
                    "titre": titre,
                    "auteur": auteur,
                    "annee": int(annee),
                    "disponible": disponible == "True"
                }
                bibliotheque.append(livre)
    except FileNotFoundError:
        print("Fichier non trouvé.")
    return bibliotheque
           
def exporter_bibliotheque (bibliotheque , chemin = "export.txt") :
    if bibliotheque is None :
        bibliotheque = []
    try:
        with open(chemin, "w") as f:
            for l in bibliotheque :
                f.write(f"{l['titre']};{l['auteur']};{l['annee']};{l['disponible']}\n")
        print(f"Bibliothèque exportée vers {chemin}")
    except IOError:
        print(f"Erreur lors de l'export vers {chemin}")
    
    
    
    
