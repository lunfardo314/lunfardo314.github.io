## Tuple trees
When composing a transaction, we aim to operate with the most generic data structures possible:
* a *byte array* (or *byte string*). *Byte array* may be empty, i.e. of zero length. Byte array can have any length (not exceeding practical limits set by the protocol);
* a *tuple* $(e_0, \dots e_{n-1})$, where each $e_i$ is either a *byte array*, or a *tuple* again.

Nested *tuples* may represent a finite hierarchical data structure, a *tree*, which has byte arrays as terminal elements and tuples as interim vertices.

Proxima transactions are represented as such a tree of tuples. Let's say $T$ is such a tree. Every element in the tree has unique *path* $(i_0, \dots i_{m-1})$ which uniquely specifies place of that element in the whole structure. Empty path $()$ points to the tip of the tree, the top tuple itself. Every part of the transaction has its *path*, a unique "address" in the transaction.

For a tuple $T$, we will denote $T_i$ as it's i-th element. In the hierachical case, element with the path $(i_0, \dots i_{m-1})$ we will denote:
$$
T_{i_0,\dots i_{m-1}} = ((T_{i_0})_{i_1}\dots)_{i_{m-1}}
$$

By $len(T)$ we will denote number of elements in the tuple:
$$
T = (T_0, \dots T_{len(T)-1})
$$
Similarly, $len(b)$ is number if bytes in the byte array $b$.
