class Etudiant:
    def __init__(self,nom,age,notes = None):
        if notes is None :
            self.notes = []
        self.nom = nom
        self.age = age 
        
    def ajouter_note(self, note) :
        list_1 = self.notes
        if note < 0 :
            return f"la note {note}/20 est invalide"
        else :
            list_1.append(note)
            return "note enregistree"
    
    def moyenne(self):
        list_2 = self.notes
        m = 0
        if len(list_2) > 0 :
            for i in list_2 :
                m += i
            return m / len(list_2)
        else :
            return 0
        
    def est_admis(self):
        if self.moyenne() >= 10:
            return True
        else: 
            return False
    
    def __str__(self):
        return f"{self.nom} | ({self.age} ans) - Moyenne : {self.moyenne():.2f} \n status : {self.est_admis()}"
    

# A = Etudiant("Alex", 21)
# B = Etudiant("Marie", 20)
# C = Etudiant("Paul", 22)

# promo = [A,B,C]

# A.ajouter_note(17)
# A.ajouter_note(15)
# A.ajouter_note(19)

# B.ajouter_note(11)
# B.ajouter_note(10)
# B.ajouter_note(7)

# C.ajouter_note(20)
# C.ajouter_note(19)
# C.ajouter_note(19.5)

# for e in promo :
#     print(e)
