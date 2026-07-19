# include "livre.h"
# include <iostream>
# include <string>
using namespace std;

int main (){

    Livre* bibliotheque[10];
    int nb = 0;

    int choix;
    do {
        cout <<"\n===== BIBLIOTHEQUE ====="<< endl;
        cout <<"\n1. Ajouter un livre"<< endl;
        cout <<"\n2. Afficher tout les livres"<< endl;
        cout <<"\n3. Chercher un livre"<< endl;
        cout <<"\n4. Livres recent"<< endl;
        cout <<"\n5. Quitter"<< endl;
        cout <<"\nVotre choix: ";
        cin >> choix;

        switch(choix){
            case 1: {
                if (nb < 10) {
                    string titre,auteur;
                    int annee,pages;
                    cout << "Titre: ";
                    cin.ignore();
                    getline(cin,titre);
                    cout << "Auteur: ";
                    cin >> auteur;
                    cout << "Année: ";
                    cin >> annee;
                    cout << "Pages: ";
                    cin >> pages;
                    bibliotheque[nb] = new Livre(titre, auteur, annee, pages);
                    nb++;   
                } else {
                    cout << "La bibliothèque est pleine." << endl;
                }
            }
            break;
            case 2: {
                for (int i = 0; i < nb; i++) {
                    bibliotheque[i]->afficher();
                }
            }
            break;
            case 3: {
                string titre;
                cout << "Titre du livre à chercher: ";
                cin >> titre;
                bool trouve = false;
                for (int i = 0; i < nb; i++) {
                    if (bibliotheque[i]->get_titre() == titre) {
                        bibliotheque[i]->afficher();
                        trouve = true;
                        break;
                    }
                }
                if (!trouve) {
                    cout << "Livre non trouvé." << endl;
                }
            }
            break;
            case 4: {
                for (int i = 0; i < nb; i++) {
                    if (bibliotheque[i]->est_recent()) {
                        bibliotheque[i]->afficher();
                    }
                }
            }
            break;
            case 5: {
                cout << "Au revoir!" << endl;
            }
            break;
            default: {
                cout << "Choix invalide." << endl;
            }
        }

    } while (choix != 5);

    return 0;
}