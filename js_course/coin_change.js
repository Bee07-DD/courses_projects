/**
 * @param {number[]} coins
 * @param {number} amount
 * @return {number}
 */
var coinChange = function(coins, amount) {
  // dp[i] contiendra le min de pièces pour former le montant i
  // On initialise avec amount + 1 (valeur sentinelle représentant l'infini)
  const dp = new Array(amount + 1).fill(amount + 1);

  // 0 pièce requise pour une somme de 0
  dp[0] = 0;

  // On calcule les solutions optimales du plus petit sous-problème au montant cible
  for (let i = 1; i <= amount; i++) {
    for (const coin of coins) {
      if (i - coin >= 0) {
        dp[i] = Math.min(dp[i], dp[i - coin] + 1);
      }
    }
  }

  // Si dp[amount] n'a pas pu être réduit, le montant est impossible à former
  return dp[amount] > amount ? -1 : dp[amount];
};
