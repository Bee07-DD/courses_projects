from etudiant import Etudiant 

class EtudiantBourse (Etudiant) :
    def __init__(self,nom,age,montant_B,notes = None):
        super().__init__(nom,age,notes)
        self.montant_B = montant_B
    
    def __str__(self):
        return super().__str__() + f"-Bourse de {self.montant_B} Fcfa"
    
A = EtudiantBourse ("Alex",18,1000000)
B = EtudiantBourse ("Malcolm",25,15000)
C = Etudiant("Alice", 21)
D = Etudiant("Marie", 20)
E = Etudiant("Paul", 22)

promo = [A,B,C,D,E]

A.ajouter_note(17)
A.ajouter_note(15)
A.ajouter_note(19)

B.ajouter_note(11)
B.ajouter_note(10)
B.ajouter_note(7)

C.ajouter_note(20)
C.ajouter_note(19)
C.ajouter_note(19.5)

D.ajouter_note(12.25)
D.ajouter_note(14)
D.ajouter_note(16)

E.ajouter_note(9)
E.ajouter_note(7.75)
E.ajouter_note(2)

promo_triee = sorted (promo,key = lambda e : e.moyenne(),reverse=True)
for e in promo_triee :
    print (e)

admis = list(filter(lambda e : e.est_admis(),promo))
for e in admis :
    print(e)