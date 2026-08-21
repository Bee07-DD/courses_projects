/**
 * @param {string} s
 * @return {number}
 */
var lengthOfLongestSubstring = function(s) {
  let maxLength = 0;
  let left = 0;
  
  // Stocke : caractère -> son dernier index vu
  const lastSeen = new Map();

  for (let right = 0; right < s.length; right++) {
    const char = s[right];

    // Si le caractère est déjà dans la fenêtre active, on saute directement après lui
    if (lastSeen.has(char) && lastSeen.get(char) >= left) {
      left = lastSeen.get(char) + 1;
    }

    // Mise à jour de l'indice et calcul de la taille maximale
    lastSeen.set(char, right);
    maxLength = Math.max(maxLength, right - left + 1);
  }

  return maxLength;
};
