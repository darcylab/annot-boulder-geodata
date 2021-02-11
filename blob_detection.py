import numpy as np
from matplotlib import image as mpimg
from skimage import morphology, measure

n_bit = 2 ** 8 - 1
n_image = 8

colors = np.load("data/colors.npy")

for ind in range(1, n_image + 1):
    img = mpimg.imread(f"data/{ind}_4_colors.png")
    green = (img[:, :, 1] * n_bit).astype(int)
    bw = green == colors[3, 1]
    bw = morphology.remove_small_holes(bw, 256)
    bw = morphology.remove_small_objects(bw, 256)
    bw = morphology.opening(bw, selem=morphology.disk(9))
    bw = morphology.erosion(bw, selem=morphology.disk(3))
    label = measure.label(bw, connectivity=1)
