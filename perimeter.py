from math import sqrt

def getInfo(x1, y1, x2, y2):
   return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def perimeter(points):
   N = len(points)
   firstx, firsty = points[0]
   prevx, prevy = firstx, firsty
   res = 0

   for i in range(1, N):
      nextx, nexty = points[i]
      res = res + getInfo(prevx,prevy,nextx,nexty)
      prevx = nextx
      prevy = nexty
   res = res + getInfo(prevx,prevy,firstx,firsty)
   return res