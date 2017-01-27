import utils
import sudoku_convert
import nrook
import numpy as np
import sudoku
import itertools
import copy

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
    value0 = sudoku_convert.nparray_to_value(nparray)
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
            action_done = nrook.nrook(nparray[i],2) or action_done
            action_done = nrook.nrook(nparray102[i],2) or action_done
        nparray = sudoku.w_transform(nparray)
        for i in range(sudoku_convert.board_size):
            action_done = nrook.nrook(nparray[i],2) or action_done
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

#def eliminate(values):
#    pass

#def only_choice(values):
#    pass

def reduce_puzzle(values,enable_diag):
    nparray = sudoku_convert.value_to_nparray(values)
    while(True):
        good = False
        good = good or reduce_puzzle_nrook(nparray,1,1,False,enable_diag)
        good = good or sub_group_exclusion(nparray,True)
        good = good or reduce_puzzle_nrook(nparray,2,2,True,enable_diag)
        good = good or reduce_puzzle_nrook(nparray,3,2,True,enable_diag)
        good = good or reduce_puzzle_nrook(nparray,4,2,True,enable_diag)
        if not good:
            break
        assign_value_nparray(values, nparray)
        if np.count_nonzero(nparray) == 81:
            break
    nparray_any2_all = np.any(nparray,2).all()
    return values if nparray_any2_all else False

def reduce_puzzle_nrook(nparray,level,min_level,ret_when_ok,enable_diag):
    # print('reduce_puzzle_nrook {}'.format(level))
    ret = False
    for axis in itertools.permutations(range(3)):
        nparray0 = np.moveaxis(nparray,range(3),axis)
        ret = reduce_puzzle_nrook_all(nparray0,level,min_level,ret_when_ok) or ret
        if ret and ret_when_ok:
            return True
    if enable_diag:
        nparray0 = sudoku.pick_diag(nparray)
        ret = reduce_puzzle_nrook_all(nparray0,level,min_level,ret_when_ok) or ret
        sudoku.put_diag(nparray,nparray0)
        if ret and ret_when_ok:
            return True
    ret = reduce_puzzle_nrook_w(nparray,level,min_level,ret_when_ok) or ret
    if ret and ret_when_ok:
        return True
    return ret

def reduce_puzzle_nrook_w(nparray,level,min_level,ret_when_ok):
    nparray0 = sudoku.w_transform(nparray)
    ret = False
    ret = (ret_when_ok and ret) or reduce_puzzle_nrook_all(nparray0,level,min_level,ret_when_ok) or ret
    ret = (ret_when_ok and ret) or reduce_puzzle_nrook_all(np.moveaxis(nparray0,range(3),[0,2,1]),level,min_level,ret_when_ok) or ret
    if not ret:
        return ret
    nparray1 = sudoku.w_transform_reverse(nparray0)
    np.copyto(nparray,nparray1)
    return ret

def reduce_puzzle_nrook_all(nparray0,level,min_level,ret_when_ok):
    ret = False
    for nparray0_i in nparray0:
        ret = nrook.nrook(nparray0_i,level,min_level) or ret
        if ret and ret_when_ok:
            return ret
    return ret

def sub_group_exclusion(nparray,ret_when_ok):
    # print('sub_group_exclusion')
    ret = False
    ret = (ret_when_ok and ret) or sub_group_exclusion_0(nparray) or ret
    ret = (ret_when_ok and ret) or sub_group_exclusion_0(np.moveaxis(nparray,range(3),[1,0,2])) or ret
    return ret

def sub_group_exclusion_0(nparray):
    ret = False
    nparray_v = sudoku.v_transform(nparray)
    nparray_vt = np.moveaxis(nparray_v,range(3),[0,2,1])
    while(True):
        ret_i = False
        ret_i = reduce_puzzle_nrook_all(nparray_v,1,1,False) or ret_i
        ret_i = reduce_puzzle_nrook_all(nparray_vt,1,1,False) or ret_i
        ret = ret or ret_i
        if not ret_i:
            break
    if not ret:
        return ret
    nparray0 = sudoku.v_transform_reverse(nparray_v)
    np.logical_and(nparray,nparray0,nparray)
    return ret

def search(values,enable_diag):
    # print('search')
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    x = reduce_puzzle(values,enable_diag)
    if x == False:
        return False

    # Chose one of the unfilled square s with the fewest possibilities
    min_box = None
    min_len = 999
    for k,v in values.items():
        if len(v) <= 1:
            continue
        if len(v) >= min_len:
            continue
        min_box = k
        min_len = len(v)

    if min_box == None:
        return values

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for c in list(values[min_box]):
        values0 = copy.copy(values)
        values0[min_box] = c
        x = search(values0,enable_diag)
        if x != False:
            values.update(x)
            return values

    # If you're stuck, see the solution.py tab!
    return False

def solve(grid,enable_diag=True):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid),enable_diag)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
