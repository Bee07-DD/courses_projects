/**
 * @param {string} start
 * @param {string} end
 * @return {boolean}
 */
var canTransform = function(start, end) {
  let i = 0;
  let j = 0;
  const n = start.length;

  while (i < n || j < n) {
    // Ignorer les 'X'
    while (i < n && start[i] === 'X') i++;
    while (j < n && end[j] === 'X') j++;

    // Si les deux atteignent la fin en même temps, c'est valide
    if (i === n && j === n) return true;
    // Si l'un termine avant l'autre, les séquences de L/R diffèrent
    if (i === n || j === n) return false;

    // Les caractères doivent correspondre
    if (start[i] !== end[j]) return false;

    // 'R' ne peut que se déplacer vers la droite (i <= j)
    if (start[i] === 'R' && i > j) return false;

    // 'L' ne peut que se déplacer vers la gauche (i >= j)
    if (start[i] === 'L' && i < j) return false;

    i++;
    j++;
  }

  return true;
};
