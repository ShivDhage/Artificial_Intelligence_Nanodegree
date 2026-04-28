
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[rows[i] + cols[i] for i in range(9)],  # main diagonal (A1 to I9)
                  [rows[i] + cols[8-i] for i in range(9)]]  # anti-diagonal (A9 to I1)
unitlist = row_units + column_units + square_units + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # Create a deep copy to avoid mutating the input
    import copy
    out = copy.deepcopy(values)
    
    # Find all naked twins (boxes with exactly 2 possibilities)
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    
    # Find pairs of twins
    for boxA in potential_twins:
        for boxB in peers[boxA]:
            # Check if boxB is also a potential twin and has the same values as boxA
            if boxB in potential_twins and values[boxA] == values[boxB]:
                # Get the intersection of peers of both boxes
                common_peers = peers[boxA] & peers[boxB]
                
                # Eliminate the digits from all common peers
                for digit in values[boxA]:
                    for peer in common_peers:
                        out[peer] = out[peer].replace(digit, '')
    
    return out


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # Find all boxes with single digit (assigned values)
    assigned_values = {box: values[box] for box in values.keys() if len(values[box]) == 1}
    
    # For each assigned box, eliminate the value from peers
    for box, value in assigned_values.items():
        for peer in peers[box]:
            values[peer] = values[peer].replace(value, '')
    
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            # Find all boxes in the unit that can have this digit
            dplaces = [box for box in unit if digit in values[box]]
            # If only one box can have this digit, assign it
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        # Apply constraint strategies
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        
        # Check how many boxes have a determined value after applying strategies
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were assigned, we've stalled
        stalled = solved_values_before == solved_values_after
        
        # Check for contradictions (empty box with no possibilities)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First reduce the puzzle with constraint strategies
    values = reduce_puzzle(values)
    
    # If reduction led to a contradiction, return False
    if values is False:
        return False
    
    # Check if puzzle is solved
    if all(len(values[box]) == 1 for box in values.keys()):
        return values
    
    # Find the unsolved box with the fewest possibilities
    min_len = 10
    min_box = None
    for box in values.keys():
        if 1 < len(values[box]) < min_len:
            min_len = len(values[box])
            min_box = box
    
    # Try each possible value for the box with fewest possibilities
    for digit in values[min_box]:
        # Create a copy and assign the digit
        new_values = values.copy()
        new_values[min_box] = digit
        
        # Recursively search
        result = search(new_values)
        if result:
            return result
    
    return False


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
