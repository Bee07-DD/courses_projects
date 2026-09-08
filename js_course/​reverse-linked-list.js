/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var reverseList = function(head) {
  let prev = null;
  let curr = head;

  while (curr !== null) {
    // 1. Sauvegarder le nœud suivant avant de rompre le lien
    const nextTemp = curr.next;

    // 2. Inverser le pointeur du nœud courant vers l'arrière
    curr.next = prev;

    // 3. Décaler les pointeurs d'un rang vers l'avant
    prev = curr;
    curr = nextTemp;
  }

  // prev pointe désormais vers l'ancienne queue, devenue la nouvelle tête
  return prev;
};
