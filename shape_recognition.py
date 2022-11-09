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
   # gaussian blur already converts image to greyscale
   processed = gaussian_blurv2(img_arr, 3, 2)
   processed = canny_edge_detection(processed)

   contours = find_contours(processed)
   draw_contour(img, (255,255,0), contours[7])

   peri = perimeter(contours[7])

   points = rdp(contours[7], peri * 0.03)
   
   return img, points


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

   images = ['triangle', 'square', 'hexagon', 'octagon']

   fig = plt.figure(figsize=(20, 20))
   fig.tight_layout()
   rows = 2
   columns = 2 

   for ndx, image in enumerate(images):
      img = Image.open('images/'+ image + '.png')
      processed_img, points = process_img(img) 
      shape_name = shape(points)

      # print(points)
      # print([tuple(y/50 for y in x) for x in points])

      fig.add_subplot(rows, columns, ndx + 1)
      plt.title(shape_name)
      plt.imshow(img)
      # plt.axis('off')

   plt.show()


main()


# img = Image.open('images/'+ 'circle' + '.png')
# processed_img, points = process_img(img) 
# shape_name = shape(points)

# print(points)
# print([tuple(y/50 for y in x) for x in points])

# img.show()