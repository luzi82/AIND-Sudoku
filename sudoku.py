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

def v_transform(nparray):
    nparray = np.reshape(nparray,[3,3,9,9])
    nparray = np.any(nparray,axis=1)
    nparray = np.moveaxis(nparray,range(3),[2,1,0])
    nparray = np.reshape(nparray,[27,3,3])
    return nparray

def v_transform_reverse(nparray):
    nparray = np.reshape(nparray,[9,9,3])
    nparray = np.moveaxis(nparray,range(3),[2,1,0])
    nparray = np.reshape(nparray,[3,1,9,9])
    nparray = np.repeat(nparray,3,axis=1)
    nparray = np.reshape(nparray,[9,9,9])
    return nparray

def pick_diag(nparray):
    diag = np.zeros([2,9,9],dtype=np.bool)
    for i in range(9):
        np.copyto(diag[0][i], nparray[i][i])
        np.copyto(diag[1][i], nparray[i][8-i])
    return diag

def put_diag(nparray,diag):
    for i in range(9):
        np.logical_and(nparray[i][i],   diag[0][i], nparray[i][i])
        np.logical_and(nparray[i][8-i], diag[1][i], nparray[i][8-i])

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

        def test_w_transform_reverse(self):
            diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
            values = utils.grid_values(diagonal_grid)
            nparray = sudoku_convert.value_to_nparray(values)
            nparray0 = w_transform(nparray)
            nparray1 = w_transform_reverse(nparray0)
            self.assertEqual(np.logical_xor(nparray, nparray1).any(),False)

        def test_v_transform(self):
            '''
            .........
            .........
            .........
            .........
            .........
            .........
            ...987...
            ...965...
            ...9.3...
            '''
            diagonal_grid = '.........................................................987......965......9.3...'
            values = utils.grid_values(diagonal_grid)
            nparray = sudoku_convert.value_to_nparray(values)
            nparray0 = v_transform(nparray)
            self.assertEqual(nparray0.shape,(27,3,3))
            nparray1 = np.reshape(nparray0,[9,3,3,3])
            self.assertEqual(nparray1[8][1][0][2],True)
            self.assertEqual(nparray1[7][1][0][2],False)
            self.assertEqual(nparray1[0][1][1][2],True)
            self.assertEqual(nparray1[7][1][1][2],True)
            self.assertEqual(nparray1[0][1][2][2],False)
            self.assertEqual(nparray1[1][1][2][2],False)
            self.assertEqual(nparray1[2][1][2][2],True)
            self.assertEqual(nparray1[4][1][2][2],True)
            self.assertEqual(nparray1[6][1][2][2],True)

        def test_v_transform_reverse(self):
            diagonal_grid = '.........................................................987......965......9.3...'
            values = utils.grid_values(diagonal_grid)
            nparray = sudoku_convert.value_to_nparray(values)
            nparray0 = v_transform(nparray)
            nparray1 = v_transform_reverse(nparray0)
            self.assertEqual(nparray1[6][3][0],False)
            self.assertEqual(nparray1[6][3][8],True)
            self.assertEqual(nparray1[6][4][0],True)
            self.assertEqual(nparray1[6][4][8],True)
            self.assertEqual(nparray1[8][4][0],True)
            self.assertEqual(nparray1[8][4][8],True)
            self.assertEqual(nparray1[7][5][5],False)
            self.assertEqual(nparray1[7][5][6],True)
            self.assertEqual(nparray1[7][5][7],False)

        def test_pick_diag(self):
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
            nparray0 = pick_diag(nparray)

            self.assertEqual(nparray0[0][0][0],False)
            self.assertEqual(nparray0[0][0][1],True)
            self.assertEqual(nparray0[0][1][0],True)
            self.assertEqual(nparray0[0][1][8],True)
            self.assertEqual(nparray0[0][2][0],True)
            self.assertEqual(nparray0[0][2][8],False)
            self.assertEqual(nparray0[0][3][0],True)
            self.assertEqual(nparray0[0][3][8],True)
            self.assertEqual(nparray0[0][4][0],False)
            self.assertEqual(nparray0[0][4][8],True)
            self.assertEqual(nparray0[0][5][0],True)
            self.assertEqual(nparray0[0][5][8],True)
            self.assertEqual(nparray0[0][6][0],False)
            self.assertEqual(nparray0[0][6][7],True)
            self.assertEqual(nparray0[0][7][0],True)
            self.assertEqual(nparray0[0][7][8],True)
            self.assertEqual(nparray0[0][8][0],False)
            self.assertEqual(nparray0[0][8][2],True)

            self.assertEqual(nparray0[1][0][0],True)
            self.assertEqual(nparray0[1][0][8],True)
            self.assertEqual(nparray0[1][1][0],True)
            self.assertEqual(nparray0[1][1][8],True)
            self.assertEqual(nparray0[1][2][0],True)
            self.assertEqual(nparray0[1][2][8],True)
            self.assertEqual(nparray0[1][3][0],False)
            self.assertEqual(nparray0[1][3][7],True)
            self.assertEqual(nparray0[1][4][0],False)
            self.assertEqual(nparray0[1][4][8],True)
            self.assertEqual(nparray0[1][5][0],False)
            self.assertEqual(nparray0[1][5][5],True)
            self.assertEqual(nparray0[1][6][0],True)
            self.assertEqual(nparray0[1][6][8],True)
            self.assertEqual(nparray0[1][7][0],True)
            self.assertEqual(nparray0[1][7][8],True)
            self.assertEqual(nparray0[1][8][0],True)
            self.assertEqual(nparray0[1][8][8],True)

        def test_put_diag(self):
            diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
            values = utils.grid_values(diagonal_grid)
            nparray = sudoku_convert.value_to_nparray(values)
            nparray0 = pick_diag(nparray)
            
            nparray0[0][1][3] = False
            nparray0[0][7][5] = False
            nparray0[1][2][1] = False
            nparray0[1][8][0] = False
            
            put_diag(nparray,nparray0)
            self.assertEqual(nparray[1][1][3],False)
            self.assertEqual(nparray[1][1][0],True)
            self.assertEqual(nparray[7][7][5],False)
            self.assertEqual(nparray[7][7][0],True)
            self.assertEqual(nparray[2][6][1],False)
            self.assertEqual(nparray[2][6][0],True)
            self.assertEqual(nparray[8][0][0],False)
            self.assertEqual(nparray[8][0][8],True)

    unittest.main()
