import numpy as np
from matplotlib import image as mpimg
from matplotlib import pyplot as plt
from OSMPythonTools.api import Api

api = Api()

# load transform matrix
geo2ind = np.load("data/geo2ind.npy")

# load piste d'Argenton
way_ids = [111415872, 235094917, 526991326, 235094922, 235094924, 235094919]

track_lat = []
track_lon = []
for way_id in way_ids:
    way = api.query("way/" + str(way_id))
    for node in way.nodes():
        track_lat.append(node.lat())
        track_lon.append(node.lon())

# get track as image indices
track_col, track_row = geo2ind @ np.stack(
    (track_lat, track_lon, np.ones_like(track_lat))
)

# load image
general_map = mpimg.imread("img/plan_general.jpg")

# overlay OSM track over map image
plt.imshow(np.mean(general_map, axis=2), cmap="gray")
plt.plot(track_col, track_row, c="#ff7900cd")
plt.axis("off")
plt.savefig("visual_check.png", dpi=300, bbox_inches="tight")
