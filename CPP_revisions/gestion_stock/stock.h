#pragma once 

#include "article.h"
#include <string>
using namespace std;

class Stock {


    // __SECTION PUBLIC__ //

    private:
    Article articles[100];
    int nbArticles;

    public:
    Stock ();
    bool ajouter(Article a) ;
    void afficherTout() const;
    double valueTotale() const;
    int rechercher(string nom) const;
};