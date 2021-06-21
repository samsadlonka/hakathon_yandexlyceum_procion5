def func(x0, y0, x1, y1): #x0, yo - координаты начала, x1, y1 - координаты конца
    deltax = abs(x1 - x0)
    deltay = abs(y1 - y0)
    error = 0
    deltaerr = (deltay + 1)
    y = y0
    diry = y1 - y0
    if diry > 0:
        diry = 1
    if diry < 0:
        diry = -1
    arr = []
    for x in range(x0, x1 + 1):
        arr.append([x, y])
        error = error + deltaerr
        if error >= (deltax + 1):
            y = y + diry
            error = error - (deltax + 1)
    x = x0
    deltaerr = (deltax + 1)
    error = 0
    dirx = x1 - x0
    if dirx > 0:
        dirx = 1
    if dirx < 0:
        dirx = -1
    for y in range(y0, y1 + 1):
        if [x, y] not in arr:
            arr.append([x, y])
        error = error + deltaerr
        if error >= (deltay + 1):
            x = x + dirx
            error = error - (deltay + 1)
    return arr
def server_function(x0, y0, z0, x1, y1, z1, mapSize = -1):
    dx = abs(x1 - x0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    dy = abs(y1 - y0)
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    dz = abs(z1 - z0)
    if z0 < z1:
        sz = 1
    else:
        sz = -1
    dm = max([1, dx, dy, dz])
    i = dm
    x1 = dm / 2
    y1 = dm / 2
    z1 = dm / 2
    line = []
    while 1:
        if mapSize != -1:
            if x0 < 0 or x0 >= mapSize:
                break
            if y0 < 0 or y0 >= mapSize:
                break
            if z0 < 0 or z0 >= mapSize:
                break
        line.append((x0, y0, z0))
        if i == 0 and mapSize == -1:
            break
        i -= 1
        x1 -= dx
        if x1 < 0:
            x1 += dm
            x0 += sx
        y1 -= dy
        if y1 < 0:
            y1 += dm
            y0 += sy
        z1 -= dz
        if z1 < 0:
            z1 += dm
            z0 += sz
    return line


def f(x0, y0, z0, x1, y1, z1):       #координаты начала и конца отрезка
    z = func(x0, y0, x1, y1)
    y = func(x0, z0, x1, z1)
    arr = []
    for i in z:
        for j in y:
            if i[0] == j[0]:
                arr.append(i[:2] + [j[1]])
    x = func(z0, y0, z1, y1)
    for i in z:
        for j in x:
            if i[1] == j[1] and i[:2] + [j[0]] not in arr:
                arr.append(i[:2] + [j[0]])
    for i in y:
        for j in x:
            if i[1] == j[0] and [i[0], j[1], j[0]] not in arr:
                arr.append([i[0], j[1], j[0]])
    return arr
if __name__ == '__main__':
    #p = f(1, 1, 1, 4, 1, 1) #[[x, y, z],  [i[0], j[1], j[0]], ...] координаты которые пересекает отрезок
    #p.sort()
    '''сортировка тут, чтобы потом не тратить время,
    т.к. при проверке координат корабля будет просто if ship in list,
    поэтому сортировка будет тратой времени, но для визуализации её можно отдельно дописать'''
    #print(p)