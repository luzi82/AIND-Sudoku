import utils
import sudoku_convert
import ntower
import numpy as np
import sudoku

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
    pass

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
