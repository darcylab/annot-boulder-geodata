import numpy as np
import pandas as pd
import cv2 as cv

# load POI
osm_df = pd.read_csv("poi/osm_poi.csv")
img_df = pd.read_csv("poi/map_img_poi.csv")

# convert to arrays
lat = osm_df.lat.values
lon = osm_df.lon.values
col = img_df.col.values
row = img_df.row.values

geo = np.stack((lat, lon)).T  # geographic coordinates
ind = np.stack((col, row)).T  # pixel indices

# estimate affine transform matrix using RANSAC algorithm
geo2ind = cv.estimateAffine2D(cv.UMat(geo), cv.UMat(ind))[0]
ind2geo = np.linalg.inv(np.vstack((geo2ind, [0, 0, 1])))[:2]  # inverse matrix

# save transform matrix
np.save("data/geo2ind.npy", geo2ind)
np.save("data/ind2geo.npy", ind2geo)
