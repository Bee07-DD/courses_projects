#pragma once

#include <string>
using namespace std;

class Article {
    

    // __SECTION PRIVATE___ //

    private:
    string nom;
    double prix;
    int quantite;

    // __SECTION PUBLIC__//

    public:
    // constructeur
    Article(string n, double p,int q);

    // les getters
    string getNom() const;
    double getPrix() const;
    int getQuantite() const;

    // le setter
    void setQuantite(int q);

    // methodes
    double valuestock() const;
    void afficher() const;






};