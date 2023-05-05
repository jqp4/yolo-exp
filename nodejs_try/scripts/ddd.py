import sys
from PIL import Image
from numpy import asarray
 
filename = sys.argv[1]
 
# load the image and convert into
# numpy array
img = Image.open(filename)
numpydata = asarray(img)
 
# data
print(numpydata)