import random


#This function is called when setting up mineField, it returns field dict
#with random placed mines on it, and fill adjacent cells with numbers

#filling empty field with mines randomly
def fillMines(rows, columns, mines, field):
    x, y = 0, 0
    while(mines != 0):
        x = random.randint(0, rows-1)
        y = random.randint(0, columns-1)
        if field[str(x)][str(y)]['0'] != 9:
            field[str(x)][str(y)]['0'] = 9
            field[str(x)][str(y)]['1'] = True
            mines -= 1
    return field

#this function will count mines on cells that are empty and adjacent to mines
def countNeighbourMines(d, f, field, rows, columns):
    mineCounter = 0
    if ((f+1 <= columns-1) and (field[str(d)][str(f+1)]['0'] == 9)):
        mineCounter += 1

    if ((f+1 <= columns-1) and (d-1 != -1) and (field[str(d-1)][str(f+1)]['0'] == 9)):
        mineCounter += 1

    if ((d-1 != -1) and (field[str(d-1)][str(f)]['0'] == 9)):
        mineCounter += 1

    if ((d-1 != -1) and (f-1 != -1) and (field[str(d-1)][str(f-1)]['0'] == 9)):
        mineCounter += 1

    if ((f-1 != -1) and (field[str(d)][str(f-1)]['0'] == 9)):
        mineCounter += 1

    if ((d+1 <= rows-1) and (f-1 != -1) and (field[str(d+1)][str(f-1)]['0'] == 9)):
        mineCounter += 1

    if ((d+1 <= rows-1) and (field[str(d+1)][str(f)]['0'] == 9)):
        mineCounter += 1

    if ((d+1 <= rows-1) and (f+1 <= columns-1) and (field[str(d+1)][str(f+1)]['0'] == 9)):
        mineCounter += 1

    return mineCounter



def createMineField(rows, columns, mines):
    field = {}
    for i in range(0, rows):
        field[str(i)] = {}
        for j in range(0, columns):
            field[str(i)][str(j)] = { '0' : 0, '1' : True}

    field = fillMines(rows, columns, mines, field)

    for i in range(0, rows):
        for j in range(0, columns):
            if(field[str(i)][str(j)]['0'] != 9):
                field[str(i)][str(j)]['0'] = countNeighbourMines(i, j, field, rows, columns)
                field[str(i)][str(j)]['1'] = True

    return field
