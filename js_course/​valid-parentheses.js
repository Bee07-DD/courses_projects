/**
 * @param {string} s
 * @return {boolean}
 */
var isValid = function(s) {
  // Une longueur impaire ne peut jamais être équilibrée
  if (s.length % 2 !== 0) return false;

  const stack = [];
  const matching = {
    '(': ')',
    '{': '}',
    '[': ']'
  };

  for (let i = 0; i < s.length; i++) {
    const char = s[i];

    // Si c'est un caractère ouvrant, on empile le fermant attendu
    if (matching[char]) {
      stack.push(matching[char]);
    } else {
      // Si c'est un fermant, il doit correspondre au sommet dépilé
      if (stack.pop() !== char) {
        return false;
      }
    }
  }

  // La chaîne est valide uniquement si tous les ouvrants ont été fermés
  return stack.length === 0;
};
