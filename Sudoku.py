import json

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
   
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):  
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values_original(grid):
    return dict(zip(boxes, grid))

def grid_values(grid):
    values = []
    for c in grid:
        if c == '.':
            values.append('123456789')
        elif c in '123456789':
            values.append(c)
    return dict(zip(boxes, values))

def eliminate(values):


    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_sudoku(values):
    stalled = False
    while not stalled:
        
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

       
        values = eliminate(values)

        
        values = only_choice(values)

       
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
       
        stalled = solved_values_before == solved_values_after
      
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

#Todos los posibles valores que pueden ir en cada casilla
example='36..2..89...361............8.3...6.24..6.3..76.7...1.8............418...97..3..14'
print("Sudoku a resolver")
display(grid_values_original(example))
print("\n Posibles numeros que pueden ir en esa casilla")
display(reduce_sudoku(grid_values(example)))

#Backtraking algoritmo
def search(values):
    values = reduce_sudoku(values)
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values 

    unfilled_squares= [(len(values[s]), s) for s in boxes if len(values[s]) > 1]
    n,s = min(unfilled_squares)
    

    for value in values[s]:
        nova_sudoku = values.copy()
        nova_sudoku[s] = value
        attempt = search(nova_sudoku)
        if attempt:
            return attempt

def solve(grid):
 
    values = grid_values(grid)
    return search(values)

example='36..2..89...361............8.3...6.24..6.3..76.7...1.8............418...97..3..14'
display(grid_values_original(example))
display((solve(example)))

if __name__ == '__main__':

    sudoku_grid='36..2..89...361............8.3...6.24..6.3..76.7...1.8............418...97..3..14'
    
    print ("original:")
    display(grid_values_original(sudoku_grid))
    print (" ")
    print ("solución:")
    display(solve(sudoku_grid))




file = open('Sudoku9x9.txt','w')
file.write(example)
file.close()

file = open('Sudoku9x9Solucion.txt','w')
file.write(str(solve(sudoku_grid)))
file.close