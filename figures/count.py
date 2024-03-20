import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

from scipy.ndimage import morphology

data = np.load("ps.npy.txt")

labeled = label(data)
mask1 = [[1,1,1,1],
         [1,1,1,1],
         [0,0,1,1],
         [0,0,1,1],
         [1,1,1,1],
         [1,1,1,1]]

mask2 = [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ]

mask3 = [[1,1,1,1],
         [1,1,1,1],
         [1,1,0,0],
         [1,1,0,0],
         [1,1,1,1],
         [1,1,1,1]]

mask4 = np.array([
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ])

mask5 =  np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1]
    ])


erosed1 = morphology.binary_erosion(data,mask1)
dilation = morphology.binary_dilation(erosed1, mask1)
data -= dilation
obj = label(dilation).max()
print(obj)

erosed2 = morphology.binary_erosion(data,mask2)
dilation2 = morphology.binary_dilation(erosed2, mask2)
data -= dilation2
obj1 = label(dilation2).max()
print(obj1)

erosed3 = morphology.binary_erosion(data,mask3)
dilation3 = morphology.binary_dilation(erosed3, mask3)
data -= dilation3
obj2 = label(dilation3).max()
print(obj2)

erosed4 = morphology.binary_erosion(data,mask4)
dilation4 = morphology.binary_dilation(erosed4, mask4)
data -= dilation4
obj3 = label(dilation4).max()
print(obj3)


erosed5 = morphology.binary_erosion(data,mask5)
dilation5 = morphology.binary_dilation(erosed5, mask5)
data -= dilation5
obj4 = label(dilation5).max()
print(obj4)

plt.title(f"СУММА = {labeled.max()}")
plt.imshow(labeled)
plt.show()