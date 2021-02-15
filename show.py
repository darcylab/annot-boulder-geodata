import pandas as pd
from matplotlib import image as mpimg
from matplotlib import pyplot as plt
import re


def show_blob_figures(
    df: pd.DataFrame, printed: str = "blob_index", s: int = 100, dpi: int = 100
) -> None:
    image_name = ""
    for blob in df.itertuples():
        if blob.image_name is not image_name:
            if image_name:
                plt.savefig(f"data/{blob.image_index - 1}_show_blob.png", dpi=dpi)
            img = mpimg.imread(blob.image_name)
            plt.figure()
            plt.imshow(img)
        image_name = blob.image_name

        marker = f"{getattr(blob, printed)}"
        # remove "le" and "la" words, vowels and spaces 
        marker = re.sub(r"^le\s|^la\s|[aâeéèêioôuy\s]", "", marker)
        # keep first 4 characters as scatter plot marker
        marker = f"${marker[:4]}$"

        plt.scatter(blob.col, blob.row, s=s, marker=marker, c="black")
    plt.savefig(f"data/{blob.image_index}_show_blob.png", dpi=dpi)
