from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

from gaussian_blurv2 import gaussian_blurv2 
from edge_detectionv2 import canny_edge_detection
from contour_detectionv2 import find_contours, draw_contours, draw_contour
from perimeter import perimeter
from rdp import rdp


def process_img(img):

   img_arr = np.array(img)
   # gaussian blur to reduce noise 
   # gaussian blur already converts image to greyscale
   processed = gaussian_blurv2(img_arr, 3, 2)
   # extract edges to reduce the amount of data to be processed
   processed = canny_edge_detection(processed)
   # contours are defined as the line joining all the points along the boundary of an image that are having the same intensity.
   # implements suzuki contour algo
   contours = find_contours(processed)
   draw_contour(img, (255,255,0), contours[7])

   peri = perimeter(contours[7])

   # Ramer-Douglas-Peucker algorithm to reduce the number of points in a curve/line 
   # without losing the shape of the curve/line, based on some tolerance parameter 'epsilon' (ε)
   points = rdp(contours[7], peri * 0.03)
   
   return processed, points


def shape(points):
   num_points = len(points) - 1
   shapes = {
      3: 'triangle',
      4: 'rectangle',
      5: 'pentagon',
      6: 'hexagon',
      7: 'heptagon',
      8: 'octagon',
   }

   return shapes.get(num_points, "{num_points}-sided polygon")



def main():

   images = ['triangle', 'rectangle', 'hexagon', 'octagon']

   fig = plt.figure(figsize=(20, 20))
   fig.tight_layout()
   rows = 2
   columns = 2 

   for ndx, image in enumerate(images):
      img = Image.open('images/'+ image + '.png')
      processed_img, points = process_img(img) 
      shape_name = shape(points)

      print(points)
      print([tuple(x/50 for x in pt) for pt in points])

      fig.add_subplot(rows, columns, ndx + 1)
      plt.title(shape_name)
      plt.imshow(img)
      # plt.axis('off')

   plt.show()


main()


# img = Image.open('images/triangle.png')
# processed_img, points = process_img(img) 
# shape_name = shape(points)

# print(points)
# print([tuple(y/50 for y in x) for x in points])

# processed_img = Image.fromarray(processed_img)
# processed_img.show()
# img.show()