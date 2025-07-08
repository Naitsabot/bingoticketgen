import random
from typing import List


def transpose(matrix: List[List[int]]) -> List[List[int]]:
    """
    Transposes any 2dimentional a matrix of array type
    """
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def pattern_generator() -> List[List[int]]:
    """
    Generate a random pattern for a bingo ticket
    """
    pattern: List[List[int]] = []
    
    # Generate a random pattern for each column    
    for _ in range(3):
        row: List[int] = [1] * 5 + [0] * 4
        random.shuffle(row)
        pattern.append(row)
    
    # Transpose the pattern to get the columns
    pattern: List[List[int]] = transpose(pattern)
    
    # Ensure that each column has at least one number
    for col in pattern:
        if not col.count(1):
            # Find a random column with more than one number
            strong_cols: List[List[int]] = [c for c in pattern if c.count(1) > 1]
            rand_strong_col: List[int] = random.choice(strong_cols)
            rand_strong_col_indexis: List[int] = [index for index, value in enumerate(rand_strong_col) if value == 1]
            rand_strong_col_idx: int = random.choice(rand_strong_col_indexis)
            
            # Adjust the columns to ensure valid bingo pattern
            col[rand_strong_col_idx] = 1
            rand_strong_col[rand_strong_col_idx] = 0
        
    return pattern


def ticket_generator() -> List[List[str]]:
    """
    Bingo Ticket Generator
    Generates a random bingo ticket with 15 numbers:
    - 5 numbers per row, 3 rows per ticket, 9 columns per ticket
    Based on https://medium.com/@binoythomas1108/create-bingo-cards-using-pythons-csv-module-8bc90d0538c3
    """
    
    # Define the pattern for the number of entries in each column
    """ pattern = [[0,0,1], [0,1,0],[1,0,1],[1,0,0],[1,1,0],[1,1,0],[0,0,1],[0,1,1],[1,1,1]]
    random.shuffle(pattern) """ # Old static pattern
    pattern: List[List[int]] = pattern_generator() # New dynamic pattern
    
    # Generate number ranges for each column
    number_ranges: List[List[int]] = [
        list(range(1, 10)),  list(range(10, 20)), list(range(20, 30)), 
        list(range(30, 40)), list(range(40, 50)), list(range(50, 60)), 
        list(range(60, 70)), list(range(70, 80)), list(range(80, 91))
    ]
    
    # Shuffle and assign numbers to the columns based on the pattern
    ticket: List[List[str]] = [["" for _ in range(3)] for _ in range(9)]
    
    # Assign numbers to the columns
    for col in range(9):
        # Get the number of numbers to assign to the column
        num_count: int = pattern[col].count(1)
        column_numbers: List[int] = random.sample(number_ranges[col], num_count)
        column_numbers.sort()
        
        # Assign the numbers to the column
        index = 0
        for row in range(3):
            if pattern[col][row] == 1:
                ticket[col][row] = str(column_numbers[index])
                index += 1

    return ticket
