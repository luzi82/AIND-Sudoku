'''
By luzi82@gmail.com, 2017-01-25

N-Rooks problem:
That is something like "N-Queens problem"
In N-Rooks problem, we are required to put N Rook pieces to a NxN grid.
Each row and col should contain exactly one rook.

Examples:

4-rook problem
1 = True = possible location
0 = False = impossible location

Input: (level=1)
+---------+
| 1 0 0 0 |
| 1 1 1 1 |
| 1 1 1 1 |
| 1 1 1 1 |
+---------+

Output:
+---------+
| 1 0 0 0 |
| 0 1 1 1 |
| 0 1 1 1 |
| 0 1 1 1 |
+---------+


Input: (level=2)
+---------+
| 1 1 0 0 |
| 1 1 0 0 |
| 1 1 1 1 |
| 1 1 1 1 |
+---------+

Output:
+---------+
| 1 1 0 0 |
| 1 1 0 0 |
| 0 0 1 1 |
| 0 0 1 1 |
+---------+


WARNING:

The function can only fill the 0 "vertically".
It is not smart enough to handle following case:

+-------+
| 1 1 1 |
| 0 1 1 |
| 0 1 1 |
+-------+

If you want to do this, please transpose the input urself.

'''

import numpy as np
import itertools

def nrook(input_vv,level,min_level=1):
    size = len(input_vv)
    one_count_v = [np.count_nonzero(input_v) for input_v in input_vv]
    suitable_idx_v = [i for i in range(size) if (one_count_v[i] <= level) and (one_count_v[i] >= min_level)]
    if len(suitable_idx_v) < level:
        return False
    combination_vv = itertools.combinations(suitable_idx_v, level)

    non_zero_count = np.count_nonzero(input_vv)

    for combination_v in combination_vv:
        orr = np.zeros(size,dtype=bool)
        for combination in combination_v:
            orr = np.logical_or(orr,input_vv[combination])
        if np.count_nonzero(orr) > level:
            continue
        orr_not = np.logical_not(orr)
        for i in range(size):
            if i in combination_v:
                continue
            np.logical_and(input_vv[i],orr_not,input_vv[i])

    return np.count_nonzero(input_vv) != non_zero_count


if __name__ == '__main__':
    import unittest
    class TestNRook(unittest.TestCase):
        def test_n_rook(self):
            x = np.array([[1,0,0,0],[1,1,1,1],[1,1,1,1],[1,1,1,1]],dtype=np.bool)
            self.assertEqual(nrook(x,1), True)
            self.assertEqual(np.logical_xor(x, np.array([[1,0,0,0],[0,1,1,1],[0,1,1,1],[0,1,1,1]],dtype=np.bool)).any(),False)

            x = np.array([[1,1,0,0],[1,1,0,0],[1,1,1,1],[1,1,1,1]],dtype=np.bool)
            self.assertEqual(nrook(x,2), True)
            self.assertEqual(np.logical_xor(x, np.array([[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]],dtype=np.bool)).any(),False)

    unittest.main()
