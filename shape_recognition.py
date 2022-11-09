from PIL import Image
import numpy as np
from gaussian_blurv2 import gaussian_blurv2 
from edge_detectionv2 import canny_edge_detection
from contour_detectionv2 import find_contours, draw_contours, draw_contour
from perimeter import perimeter
from rdp import rdp


def process_img(img):

   img_arr = np.array(img)
   # gaussian blur already converts image to greyscale
   processed = gaussian_blurv2(img_arr, 3, 2)
   processed = canny_edge_detection(processed)

   contours = find_contours(processed)
   draw_contour(img, (255,255,0), contours[7])

   peri = perimeter(contours[7])

   test = rdp(contours[7], peri * 0.03)
   print(test)
   print([tuple(y/50 for y in x) for x in test])

   return img




img = Image.open('images/shapes5.png')
processed = process_img(img)
img.show()

exit()

img = Image.open('images/square.png')
processed = process_img(img)

img = Image.open('images/pentagon.png')
processed = process_img(img)

img = Image.open('images/hexagon.png')
processed = process_img(img)

img = Image.open('images/septagon.png')
processed = process_img(img)

img = Image.open('images/octagon.png')
processed = process_img(img)

img = Image.open('images/12.png')
processed = process_img(img)





