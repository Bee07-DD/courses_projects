// gardes d'inclusion 
// # ifndef LIVRE_H
// # define LIVRE_H

# include <string>
using namespace std;



// création de la classe avec ses paramètres 

class Livre {

    private : 
    string titre;
    string auteur;
    int annee;
    int pages;


    public :
    Livre(string titre, string auteur, int annee, int pages);
    string get_titre() const ;// paramètre disant qu'on ne modifie aucun attribut de l'objet ;
    string get_auteur() const;
    int get_annee() const;
    int get_pages() const;
    void set_pages(int new_pages);
    bool est_recent() const;
    void afficher() const ;
};

#endif 