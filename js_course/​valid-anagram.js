/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
var isAnagram = function(s, t) {
  // Deux longueurs distinctes ne peuvent pas former d'anagramme
  if (s.length !== t.length) return false;

  // Tableau de 26 cases pour les lettres 'a' à 'z'
  const charCounts = new Array(26).fill(0);
  const baseCode = 'a'.charCodeAt(0);

  // Incrémenter pour s, décrémenter pour t
  for (let i = 0; i < s.length; i++) {
    charCounts[s.charCodeAt(i) - baseCode]++;
    charCounts[t.charCodeAt(i) - baseCode]--;
  }

  // Vérifier si toutes les cases sont revenues à 0
  for (let i = 0; i < 26; i++) {
    if (charCounts[i] !== 0) {
      return false;
    }
  }

  return true;
};
