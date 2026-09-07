/**
 * @param {number[]} prices
 * @return {number}
 */
var maxProfit = function(prices) {
  let minPrice = Infinity;
  let maxProfit = 0;

  for (let i = 0; i < prices.length; i++) {
    const currentPrice = prices[i];

    // Mettre à jour le prix d'achat minimal historique
    if (currentPrice < minPrice) {
      minPrice = currentPrice;
    } else {
      // Calculer le profit potentiel si on revend à ce jour
      const currentProfit = currentPrice - minPrice;
      if (currentProfit > maxProfit) {
        maxProfit = currentProfit;
      }
    }
  }

  return maxProfit;
};
