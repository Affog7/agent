from settings import GRID_SIZE


def dernieres_coordonnees():

    if GRID_SIZE > 0 and GRID_SIZE > 0:
        coordonnees = [
            (GRID_SIZE-1, GRID_SIZE-4) if GRID_SIZE > 3 else None,
            (GRID_SIZE-1, GRID_SIZE-3) if GRID_SIZE > 2 else None,
            (GRID_SIZE-1, GRID_SIZE-2) if GRID_SIZE > 1 else None,
            (GRID_SIZE-1, GRID_SIZE-1)
        ]
        #print(coordonnees)
        return [coord for coord in coordonnees if coord is not None]
    else:
        return None