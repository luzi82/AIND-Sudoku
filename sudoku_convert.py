import utils
import numpy as np

board_size = len(utils.rows)

def value_to_nparray(values):
    ret = np.zeros((board_size,board_size,board_size),dtype=bool)
    for r in range(len(utils.rows)):
        for c in range(len(utils.cols)):
            box_key = utils.rows[r]+utils.cols[c]
            box_value = values[box_key]
            for v in range(board_size):
                ret[r][c][v] = str(v+1) in box_value
    return ret

def nparray_to_value(nparray):
    ret = {}
    for r in range(len(utils.rows)):
        for c in range(len(utils.cols)):
            box_key = utils.rows[r]+utils.cols[c]
            nparray_ii = nparray[r][c]
            ret[box_key] = ''.join([str(i+1) for i in range(board_size) if nparray_ii[i]])
    return ret

if __name__ == '__main__':
    import unittest
    import solution_test

    class SudokuConvertTest(unittest.TestCase):
        def test_value_to_nparray(self):
            diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
            values = utils.grid_values(diagonal_grid)
            nparray = value_to_nparray(values)
            self.assertEqual(nparray[0][0][0],False)
            self.assertEqual(nparray[0][0][1],True)
            self.assertEqual(nparray[0][0][2],False)
            self.assertEqual(nparray[0][1][0],True)
            self.assertEqual(nparray[0][1][8],True)
            self.assertEqual(nparray[1][5][5],True)
            self.assertEqual(nparray[1][5][4],False)
            self.assertEqual(nparray[1][5][6],False)
            
        def test_nparray_to_value(self):
            diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
            values = utils.grid_values(diagonal_grid)
            nparray = value_to_nparray(values)
            values0 = nparray_to_value(nparray)
            self.assertEqual(values,values0)

    unittest.main()
