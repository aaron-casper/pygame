aiWalls = [(25, 25), (25, 75), (25, 125)]
wallTable = []
tileX = 0
tileY = 0
row = []
tableSizeX = 200
tableSizeY = 200
while tileY < tableSizeY:
    tileX = 0
    while tileX < tableSizeX:
        pos = (tileX,tileY)
        for node in aiWalls:
            if node[0] == pos[0] and node[1] == pos[1]:
                print("wall found @ " + str(pos))
                row.append(1)
                break
        else:
            row.append(0)
        tileX = tileX + 25
    tileY = tileY + 25

    wallTable.append(row)
    row = []
for scan in wallTable:
    print(scan)
