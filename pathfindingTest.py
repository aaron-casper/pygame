from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import sqlite3
database = "maps.db"
conn = sqlite3.connect(database)

def loadNodeGraph(mapID):
    aiWalls = []
    allWalls = []
    row = []
    sqlQuery = "SELECT nodeGraph FROM nodeGraphs WHERE mapID = " + str(mapID) + ";"
    cur = conn.cursor()
    nodeGraphData = cur.execute(sqlQuery)
    for item in nodeGraphData:
        #print(item)
        #print("item")
        item = str(item).replace(',','')
        item = str(item).split('|')
        
        y = 1
        while y < len(item) - 1:
            row = []
            x = 0
            while x < len(item[y]):
                print(item[y][x],end='')
                row.append(int(item[y][x]))
                x += 1
            print('')
            aiWalls.append(row)
            y += 1
        print(aiWalls)
            
    return(aiWalls)
    
    #xdiff = targx - path[0]
    #ydiff = targy - path[1]
    #self.angle = math.atan2(ydiff,xdiff)

matrix = loadNodeGraph(1)

grid = Grid(matrix=matrix)

start = grid.node(0, 0)
end = grid.node(30, 20)

finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
path, runs = finder.find_path(start, end, grid)

print('operations:', runs, 'path length:', len(path))
print(grid.grid_str(path=path, start=start, end=end))
