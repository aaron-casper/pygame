import sqlite3
database = "./maps.db"
conn = sqlite3.connect(database)

def loadMap(mapID):

    new_walls = []
    sqlQuery = "SELECT * FROM levels WHERE mapID = " + str(mapID) + ";"
    
    cur = conn.cursor()
    levelData = cur.execute(sqlQuery)

    for item in levelData:
        for detail in item:
            #print(detail)
            if type(detail) == str:
                detail = detail.replace('[','')
                detail = detail.replace(']','')
                detail = detail.strip('|') #to prevent out of range later
                detail = detail.split('|')
 #               print(detail)
                for coordPair in detail:
                    coordPair = coordPair.split(',')
                    x = int(coordPair[0])
                    y = int(coordPair[1])
                    tileType = int(coordPair[2])
                    print(coordPair)
                    #tileType = int(coordPair[2])
                    new_walls.append((x,y,tileType))
                
    return(new_walls)
    #print(all_walls)

#print(loadMap(1))
