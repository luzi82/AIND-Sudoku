import utils
import sudoku_convert
import ntower
import numpy as np
import sudoku
import itertools

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def assign_value_nparray(values, nparray):
    value0 = nparray_to_value(nparray)
    for box in values:
        if values[box] == value0[box]:
            continue
        assign_value(values, box, value0[box])

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    nparray = sudoku_convert.value_to_nparray(values)
    while (True):
        action_done = False
        nparray102 = np.moveaxis(nparray,range(3),[1,0,2])
        for i in range(sudoku_convert.board_size):
            action_done = ntower.ntower(nparray[i],2) or action_done
            action_done = ntower.ntower(nparray102[i],2) or action_done
        nparray = sudoku.w_transform(nparray)
        for i in range(sudoku_convert.board_size):
            action_done = ntower.ntower(nparray[i],2) or action_done
        nparray = sudoku.w_transform_reverse(nparray)
        if not action_done:
            break
        break

    return sudoku_convert.nparray_to_value(nparray)

#def cross(A, B):
#    "Cross product of elements in A and elements in B."
#    pass

cross = utils.cross

#def grid_values(grid):
#    """
#    Convert grid into a dict of {square: char} with '123456789' for empties.
#    Args:
#        grid(string) - A grid in string form.
#    Returns:
#        A grid in dictionary form
#            Keys: The boxes, e.g., 'A1'
#            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
#    """
#    pass

grid_values = utils.grid_values

#def display(values):
#    """
#    Display the values as a 2-D grid.
#    Args:
#        values(dict): The sudoku in dictionary form
#    """
#    pass

display = utils.display

def eliminate(values):
    pass

def only_choice(values):
    pass

def reduce_puzzle(values):
    nparray = sudoku_convert.value_to_nparray(values)
    while(True):
        good = False
        good = good or reduce_puzzle_ntower(nparray,1,1,False)
        good = good or sub_group_exclusion(nparray)
        good = good or reduce_puzzle_ntower(nparray,2,2,True)
        good = good or reduce_puzzle_ntower(nparray,3,2,True)
        good = good or reduce_puzzle_ntower(nparray,4,2,True)
        if not good:
            break
        assign_value_nparray(values, nparray)

def reduce_puzzle_ntower(nparray,level,min_level,ret_when_ok):
    ret = False
    for axis in itertools.permutations(range(3)):
        nparray0 = np.moveaxis(nparray,range(3),axis)
        for nparray0_i in nparray0:
            ret = ntower.ntower(nparray0_i,level,min_level) or ret
            if ret and ret_when_ok:
                return True
    ret = reduce_puzzle_ntower_w(nparray,level,min_level,ret_when_ok) or ret
    if ret and ret_when_ok:
        return True
    ret = reduce_puzzle_ntower_w(np.moveaxis(nparray,range(3),[1,0,2]),level,min_level,ret_when_ok) or ret
    if ret and ret_when_ok:
        return True
    return ret

def reduce_puzzle_ntower_w(nparray,level,min_level,ret_when_ok):
    nparray0 = sudoku.w_transform(nparray)
    ret = False
    ret = (ret_when_ok and ret) or reduce_puzzle_ntower_w_0(nparray0,level,min_level,ret_when_ok) or ret
    ret = (ret_when_ok and ret) or reduce_puzzle_ntower_w_0(np.moveaxis(nparray0,range(3),[0,2,1]),level,min_level,ret_when_ok) or ret
    if not ret:
        return ret
    nparray1 = sudoku.w_transform_reverse(nparray0)
    np.copyto(nparray,nparray1)
    return ret

def reduce_puzzle_ntower_w_0(nparray,level,min_level,ret_when_ok):
    for nparray0_i in nparray0:
        ret = ntower.ntower(nparray0_i,level,min_level) or ret
        if ret and ret_when_ok:
            return True
    return ret

def sub_group_exclusion(nparray):
    ret = False
    nparray_v = sudoku.v_transform(nparray)
    nparray_vt = np.moveaxis(nparray_v,range(3),[0,2,1])
    while(True):
        ret_i = False
        for nparray_vi in nparray_v:
            ret_i = ntower.ntower(nparray_vi,1) or ret_i
        for nparray_vi in nparray_vt:
            ret_i = ntower.ntower(nparray_vi,1) or ret_i
        ret = ret or ret_i
        if not ret_i:
            break
    if not ret:
        return ret
    nparray0 = sudoku.v_transform_reverse(nparray_v)
    np.logical_and(nparray,nparray0,nparray)
    return ret

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
