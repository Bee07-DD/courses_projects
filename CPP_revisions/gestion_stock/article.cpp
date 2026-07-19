#include "article.h"
#include <iostream>

// constructeur 

Article :: Article(string n,double p,int q) {
    nom = n;
    prix = p;
    quantite = q;
}

// getters
string Article :: getNom() const {
    return nom;

}

double Article :: getPrix() const {
    return prix;
}

int Article :: getQuantite() const {
    return quantite;
}

// setter

void Article :: setQuantite(int q) {
    if (q < 0){
        cout <<"quantité invalide"<<endl;
    }
    else {
        quantite = q;
    }
}

// methodes 

double Article :: valuestock() const {
    return prix*quantite;
}

void Article :: afficher() const {
    cout << nom <<" - "<< prix <<" FCFA x "<< quantite << endl;
}