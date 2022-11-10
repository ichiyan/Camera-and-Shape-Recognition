from PIL import Image
import numpy as np


#      N      NE    E    SE    S    SW    W   NW
# direction between two pixels

# rotate direction clockwise
def clockwise(dir):
    return (dir)%8 + 1

# rotate direction counterclockwise
def counterclockwise(dir):
    return (dir+6)%8 + 1

def move(pixel, img, dir, dir_delta):
    # chk
    newp = [pixel[0] + dir_delta[dir-1][0], pixel[1] + dir_delta[dir-1][1]]
    height, width = img.shape
    if 0 <= newp[0] < height and 0 <= newp[1] < width:
        if img[newp[0]][newp[1]] != 0:
            return newp
    
    return [0,0]

# find direction between two pixels
def direction(src, dst, dir_delta):
    delta = [dst[0] - src[0], dst[1] - src[1]]
    return [i for i, v in enumerate(dir_delta) if v[0] == delta[0] and v[1] == delta[1]][0]

def detect_move(img, p0, p2, nbd, border, done, dir_delta):
    dir = direction(p0, p2, dir_delta)
    moved = clockwise(dir)
    p1 = [0,0]
    while moved != dir:
        newp = move(p0, img, moved, dir_delta)
        if newp[0] != 0:
            p1 = [newp[0], newp[1]]
            break

        moved = clockwise(moved)
    
    if p1[0] == 0 and p1[1] == 0:
        return
  
    p2 = p1
    p3 = p0 

    done = [False] * 8

    while True:
        dir = direction(p3, p2, dir_delta)
        moved = counterclockwise(dir)
        p4 = [0,0]
        done = [False] * 8

        while True:
            p4 = move(p3, img, moved, dir_delta)
            if p4[0] != 0:
                break
            done[moved-1] = True
            moved = counterclockwise(moved)
        border.append(tuple(p3))
        if p3[0] == img.shape[0] or done[2]:
            img[p3[0]][p3[1]] = -nbd
        elif img[p3[0]][p3[1]] == 1:
            img[p3[0]][p3[1]] = nbd
        
        if p4 == p0 and p3 == p1:
            break

        p2 = p3
        p3 = p4
            

def find_contours(img):

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = img[i][j] > 0.45

    nbd = 1
    lnbd = 1
    img = np.float64(img)
    contours = []
    done = [False, False, False, False, False, False, False, False]

    # Clockwise Moore neighborhood.
    dir_delta = [(-1, 0) , (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1,-1)]

    height, width = img.shape

    for i in range(0, height):
        lnbd = 1
        for j in range(0, width):
            # print(f"{i} {j}  {img[i][j]}")
            fij = img[i][j]
            #  chk
            is_outer = (img[i][j] == 1 and (j == 0 or img[i][j-1] == 0))
            is_hole = (img[i][j]>= 1 and (j == width - 1 or img[i][j+1] == 0))
            
            # print(f"outer: {is_outer}   hole: {is_hole}")
            if is_outer or is_hole:
                border = [] 
                src = [i,j]

                if is_outer:
                    nbd += 1
                    src[0] -= 0
                    src[1] -= 1

                else:
                    nbd += 1
                    if fij > 1:
                        lnbd = fij

                    src[0] += 0
                    src[1] += 1

                p0 = [i, j]
                detect_move(img, p0, src, nbd, border, done, dir_delta)
                
                if not border:
                    border.append(tuple(p0))
                    img[p0[0]][p0[1]] = -nbd
                
                contours.append(border)
            
            if fij != 0 and fij != 1:
                lnbd = abs(fij)
    
    return contours

def draw_contour(img, color, contour):
    for ndx in contour:
        img.getpixel( (ndx[1], ndx[0]) )
        img.putpixel( (ndx[1], ndx[0]), color )

def draw_contours(img, color, contours):
    for cnt in contours:
        draw_contour(img, color, cnt)



def test():
    im = np.array(Image.open('images/canny.jpg'))
    # im = np.array(Image.open('images/shapes5.png').convert('RGB'))
    # im = cv2.imread('images/shapes5.png')
    # im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    # im = np.array(im)

    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            im[i][j] = im[i][j] > 0.45


    contours = find_contours(im)

    print(len(contours))

    im = Image.fromarray(im)
    im = im.convert('RGB')
    # print(im.size)

    draw_contours(im,(255,255,0),contours)

    im.show()


    # print(type(im))

# test()