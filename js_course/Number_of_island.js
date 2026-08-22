/**
 * @param {character[][]} grid
 * @return {number}
 */
var numIslands = function(grid) {
  if (!grid || grid.length === 0) return 0;

  let count = 0;
  const rows = grid.length;
  const cols = grid[0].length;

  // Fonction récursive pour marquer toutes les terres connectées
  function sinkIsland(r, c) {
    // Vérification des limites de la grille et arrêt sur l'eau ('0')
    if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] === '0') {
      return;
    }

    // On coule la cellule pour ne plus la recompter
    grid[r][c] = '0';

    // Exploration des 4 directions cardinales
    sinkIsland(r + 1, c); // Bas
    sinkIsland(r - 1, c); // Haut
    sinkIsland(r, c + 1); // Droite
    sinkIsland(r, c - 1); // Gauche
  }

  // Parcours complet de la grille
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === '1') {
        count++;
        sinkIsland(r, c); // Coule toute l'île connectée
      }
    }
  }

  return count;
};
