function twoSum(nums, target) {
    // Création d'une map pour stocker les nombres et leurs indices
    const map = new Map();

    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];

        // Si le complément est déjà dans la map, on a trouvé la solution
        if (map.has(complement)) {
            return [map.get(complement), i];
        }

        // Sinon, on ajoute le nombre actuel et son indice dans la map
        map.set(nums[i], i);
    }

    // Renvoie un tableau vide si aucune solution n'est trouvée
    return [];
}

// --- Exemple d'utilisation ---
const exemples Nums =;
const cible = 9;
console.log(twoSum(exemplesNums, cible)); // Résultat attendu : [0, 1] (car 2 + 7 = 9)
