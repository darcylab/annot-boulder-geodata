import glob
import numpy as np
from matplotlib import image as mpimg
from matplotlib import colors
from sklearn.cluster import KMeans

# parameters
n_channel = 3
n_bit = 2 ** 8 - 1
n_cluster = 3  # black, green, orange


def rgb_to_flat_cyan_hsv(rgb: np.ndarray) -> np.ndarray:
    hsv = colors.rgb_to_hsv(rgb / n_bit).reshape((-1, n_channel))
    hsv[:, 0] = np.mod(hsv[:, 0] + 0.5, 1)  # shift hue origin to cyan
    return hsv


def flat_cyan_hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    hsv[:, 0] = np.mod(hsv[:, 0] - 0.5, 1)  # shift hue origin back to red
    rgb = colors.hsv_to_rgb(hsv.reshape(-1, 1, n_channel))
    return rgb


# get colors from reference image
ref = mpimg.imread("img/i-20eme 25eme epingle.jpg")
hsv = rgb_to_flat_cyan_hsv(ref)
saturated = hsv[:, 1] > 0.5  # keep saturated colors only
kmeans = KMeans(n_clusters=n_cluster).fit(hsv[saturated, :])
centers = flat_cyan_hsv_to_rgb(kmeans.cluster_centers_).reshape(n_cluster, n_channel)
centers = np.insert(centers, 0, [1.0, 1.0, 1.0], axis=0)  # add white background
centers = (centers * n_bit).astype(ref.dtype)
np.save("data/colors.npy", centers)  # colors LUT

# apply color quantization
submaps = glob.glob("img/i*.jpg")
submaps.sort()
submaps.insert(0, "img/plan_general.jpg")  # add general map
for ind, submap in enumerate(submaps):
    img = mpimg.imread(submap)
    hsv = rgb_to_flat_cyan_hsv(img)
    saturated = hsv[:, 1] > 0.5
    labels = np.zeros(hsv.shape[0])
    labels[saturated] = kmeans.predict(hsv[saturated, :]) + 1  # predict
    labels = centers[labels.reshape(img.shape[:2]).astype(int)]  # apply LUT
    mpimg.imsave(f"data/{ind}_4_colors.png", labels)
