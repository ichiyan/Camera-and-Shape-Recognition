import numpy as np
import ast
from PIL import Image
import cv2


# four-connected case
"""
    Direction Reference:
                1
                |
                |
         2 <- - | - -> 0
                |
                |
                3
    """
def next_cell(curr_pixel,curr_dir):
    i,j=curr_pixel
    save=None
    if curr_dir==0:
        r=i-1
        c=j
        new_dir=1
        save=[i,j+1]
    elif curr_dir==1:
        r=i
        c=j-1
        new_dir=2
    elif curr_dir==2:
        r=i+1
        c=j
        new_dir=3
    elif curr_dir==3:
        r=i
        c=j+1
        new_dir=0
    return r,c,new_dir,save

# step 2
# (i2, j2) : prev

def border_follow(img,start,prev,direction,NBD):
    curr=list(start)
    exam=list(prev)
    save=None
    save2=list(exam)
    contour=[]
    contour.append(list(curr))
    # 2.1
    while img[exam[0]][exam[1]]==0:
        exam[0],exam[1],direction,save_pixel=next_cell(curr,direction)
        if save_pixel!=None:
            save=list(save_pixel)
            # break?
        # if full rotation (non-zero pixel not found)
        if save2==exam:
            img[curr[0],curr[1]]=-NBD
            return contour
    # if non-zero pixel is found?
    if save!=None:
        img[curr[0]][curr[1]]=-NBD
        save=None
    elif (save==None or (save!=None and img[save[0]][save[1]]!=0)) and img[curr[0]][curr[1]]==1: img[curr[0]][curr[1]]=NBD
    else: pass
    # 2.2
    # prev should get i1j1?
    prev=list(curr)
    curr=list(exam)
    contour.append(list(curr))
    if direction>=2: direction=direction-2
    else: direction=2+direction
    flag=0
    start_next=list(curr)
    while True:
        if not(curr==start_next and prev==start and flag==1):
            flag=1
            exam[0],exam[1],direction,save_pixel=next_cell(curr,direction)
            if save_pixel!=None:
                save=list(save_pixel)
            try:
                while img[exam[0]][exam[1]]==0:
                    exam[0],exam[1],direction,save_pixel=next_cell(curr,direction)
                    if save_pixel!=None:
                        save=list(save_pixel)
                if save!=None and img[save[0]][save[1]]==0:
                    img[curr[0]][curr[1]]=-NBD
                    save=None
                elif (save==None or (save!=None and img[save[0]][save[1]]!=0)) and img[curr[0]][curr[1]]==1: img[curr[0]][curr[1]]=NBD
                else: pass
                prev=list(curr)
                curr=list(exam)
                contour.append(list(curr))
                if direction>=2: direction=direction-2
                else: direction=2+direction
            except IndexError:
                break
        else:
            break
    return contour
        
def raster_scan(img):
    rows,cols=img.shape
    LNBD=1
    NBD=1
    contours=[]
    parent=[]
    parent.append(-1)
    border_type=[]
    border_type.append(0)
    # should be: for i in range(0, rows) as in (0, row] 
    for i in range(1,rows-1):
        # print(i)
        LNBD=1
        # similar to first for loop?
        for j in range(1,cols-1):
            # print(j)
            # if pixels > 0 ?
            # if outer border
            if img[i][j]==1 and img[i][j-1]==0:
                NBD+=1
                direction=2
                parent.append(LNBD) 
                contour=border_follow(img,[i,j],[i,j-1],direction,NBD)
                contours.append(contour)
                border_type.append(1)
                if border_type[NBD-2]==1: parent.append(parent[NBD-2])
                else:
                    if img[i][j]!=1: LNBD=abs(img[i][j]) 
            
            # hole border  
            elif img[i][j]>=1 and img[i][j+1]==0:
                NBD+=1
                direction=0
                if img[i][j]>1: LNBD=img[i][j]
                parent.append(LNBD)
                contour=border_follow(img,[i,j],[i,j+1],direction,NBD)
                contours.append(contour)
                border_type.append(0)
                if border_type[NBD-2]==0: parent.append(parent[NBD-2])
                else:
                    if img[i][j]!=1: LNBD=abs(img[i][j])

            # lacks step 3?

    return contours,parent,border_type


def test():

    img=np.array(Image.open("images/canny.jpg"))

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # print(img.shape)
    # print(img[209][132])

    contours,parent,border_type=raster_scan(img)
    print(contours)
    print(parent)
    print(border_type)


test()

