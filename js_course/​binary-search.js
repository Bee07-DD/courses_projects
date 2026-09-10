/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number}
 */
var search = function(nums, target) {
  let left = 0;
  let right = nums.length - 1;

  while (left <= right) {
    // Calcul du milieu évitant l'éventuel débordement d'entier (left + right) / 2
    const mid = Math.floor(left + (right - left) / 2);

    if (nums[mid] === target) {
      return mid;
    } else if (nums[mid] < target) {
      // La cible est dans la moitié droite
      left = mid + 1;
    } else {
      // La cible est dans la moitié gauche
      right = mid - 1;
    }
  }

  // Cible non trouvée dans le tableau
  return -1;
};
