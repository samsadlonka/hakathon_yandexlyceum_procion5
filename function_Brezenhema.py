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

if __name__ == '__main__':
    p = func(1, 5, 11, 1)
    p.sort()
    print(p)
