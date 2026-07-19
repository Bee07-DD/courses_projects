# include "livre.h"
# include <iostream>
# include <string>
using namespace std;

// le constructeur 
Livre :: Livre (string t, string a, int an, int p){
    titre = t;
    auteur = a;
    annee = an;
    pages = p;
}

// les quatres getters 

string Livre :: get_titre() const {
    return titre ;
}

string Livre :: get_auteur() const {
    return auteur ;
}

int Livre :: get_annee() const {
    return annee ;
}

int Livre :: get_pages() const {
    return pages ;
}

// le setter 

void Livre :: set_pages (int new_pages){
    if (new_pages <= 0){
        cout << "Le nombre de pages ne peut pas être négatif." << endl;
    } else {
        pages = new_pages;
    }
}

// la fonction est_recent

bool Livre :: est_recent () const {
    if (annee > 2000) {
        return true;
    } else {
        return false;
    }

}

// affichage du livre 

void Livre :: afficher() const {
    cout << "Titre: " << titre << endl;
    cout << "Auteur: " << auteur << endl;
    cout << "Année: " << annee << endl;
    cout << "Pages: " << pages << endl;
    cout << "Est recent: " << est_recent() << endl;
}
