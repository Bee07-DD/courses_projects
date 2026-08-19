/**
 * @param {string} croakOfFrogs
 * @return {number}
 */
function minNumberOfFrogs(croakOfFrogs) {
    // Compteurs pour chaque lettre en cours
    let c = 0, r = 0, o = 0, a = 0;
    let maxFrogs = 0;
    let currentFrogs = 0;

    for (const char of croakOfFrogs) {
        if (char === 'c') {
            c++;
            currentFrogs++; // Une grenouille commence à chanter
            maxFrogs = Math.max(maxFrogs, currentFrogs);
        } else if (char === 'r') {
            if (c === 0) return -1; // Pas de 'c' précédent pour ce 'r'
            c--; r++;
        } else if (char === 'o') {
            if (r === 0) return -1;
            r--; o++;
        } else if (char === 'a') {
            if (o === 0) return -1;
            o--; a++;
        } else if (char === 'k') {
            if (a === 0) return -1;
            a--;
            currentFrogs--; // La grenouille a fini, elle est dispo pour un autre "croak"
        } else {
            return -1; // Caractère parasite
        }
    }

    // S'il reste des grenouilles qui n'ont pas fini leur "croak", la chaîne est invalide
    if (currentFrogs > 0) return -1;

    return maxFrogs;
}
