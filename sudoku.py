import numpy as np

def w_transform(nparray):
    nparray = np.reshape(nparray,[3,3,9,9])
    nparray = np.moveaxis(nparray,range(4),[0,2,1,3])
    nparray = np.reshape(nparray,[9,9,9])
    return nparray

def w_transform_reverse(nparray):
    nparray = np.reshape(nparray,[3,9,3,9])
    nparray = np.moveaxis(nparray,range(4),[0,2,1,3])
    nparray = np.reshape(nparray,[9,9,9])
    return nparray

if __name__ == '__main__':
    import unittest
    import utils
    import sudoku_convert

    class TestMe(unittest.TestCase):
        def test_w_transform(self):
            '''
            2........
            .....62..
            ..1....7.
            ..6..8...
            3...9...7
            ...6..4..
            .4....8..
            ..52.....
            ........3
            '''
            diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
            values = utils.grid_values(diagonal_grid)
            nparray = sudoku_convert.value_to_nparray(values)
            nparray0 = w_transform(nparray)
            self.assertEqual(nparray0[0][0][0],False)
            self.assertEqual(nparray0[0][0][1],True)
            self.assertEqual(nparray0[0][8][0],True)
            self.assertEqual(nparray0[0][8][1],False)
            self.assertEqual(nparray0[1][7][0],False)
            self.assertEqual(nparray0[1][7][5],True)
            self.assertEqual(nparray0[7][1][0],False)
            self.assertEqual(nparray0[7][1][1],True)

        def test_w_transform(self):
            diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
            values = utils.grid_values(diagonal_grid)
            nparray = sudoku_convert.value_to_nparray(values)
            nparray0 = w_transform(nparray)
            nparray1 = w_transform_reverse(nparray0)
            self.assertEqual(np.logical_xor(nparray, nparray1).any(),False)

    unittest.main()
