import numpy as np
import pandas as pd
import glob
from matplotlib import image as mpimg
from skimage import morphology, measure

n_bit = 2 ** 8 - 1
n_image = 8

# Morphogy operations parameters
area_threshold = 256  # arbitrary large enough
opening_radius = 9
erosion_radius = 3

colors = np.load("data/colors.npy")

submaps = glob.glob("img/i*.jpg")
submaps.sort()
submaps.insert(0, "img/plan_general.jpg")  # add general map

image_index = []
image_name = []
blob_index = []
centroid = []
for img_ind in range(1, n_image + 1):
    img = mpimg.imread(f"data/{img_ind}_4_colors.png")
    green = (img[:, :, 1] * n_bit).astype(int)  # green channel
    bw = green == colors[1, 1]  # second label from color_quantization.py

    # Morphological cleaning
    bw = morphology.remove_small_holes(bw, area_threshold)
    bw = morphology.remove_small_objects(bw, area_threshold)
    bw = morphology.opening(bw, selem=morphology.disk(opening_radius))

    # Erosion step to disconnect close blobs
    bw = morphology.erosion(bw, selem=morphology.disk(erosion_radius))

    # Get blobs centroids
    label = measure.label(bw, connectivity=1)
    regions = measure.regionprops(label)
    for b_ind, region in enumerate(regions):
        image_index.append(img_ind)
        image_name.append(submaps[img_ind])
        blob_index.append(b_ind)
        centroid.append(region.centroid)
centroid = np.array(centroid)
data = {
    "image_index": image_index,
    "image_name": image_name,
    "blob_index": blob_index,
    "col": centroid[:, 1],
    "row": centroid[:, 0],
}
df = pd.DataFrame(data)
df.to_csv("poi/blobs.csv")
