import numpy as np
import sys
sys.setrecursionlimit(30000)
from scipy import ndimage
import matplotlib.pyplot as plt
from scipy.datasets import face
from scipy.ndimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
from skimage.draw import disk
from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion

struct = np.ones((1,1))
def erosion(data,struct = struct):
    result = np.zeros_like(data)
    for y in range(1,data.shape[0]- 1):
        for x in range(1,data.shape[1] - 1):
            sub = data[y - 1 : y + 2, x-1:x+2]
            if np.all(sub == struct):
                result[y,x] = 1
    return result   

data = np.load('wires4.npy.txt')
labeled = label(data)
for lbl in range(1,labeled.max()+1):
    plt.figure()
    plt.imshow(labeled==lbl)
    count = label(binary_erosion(labeled == lbl)).max()
    if count == 0:
        print('Провод не существует')
    if count == 1:
        print('Провод не поделен')
    else:

        print(f"Провод поделен на {count}")


plt.show()
