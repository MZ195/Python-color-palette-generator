from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import argparse
import cv2


def plot_colors(centroids, width):
    # initialize the bar chart representing the colors
    img = np.zeros((50, width, 3), dtype="uint8")
    startX = 0
    offset = int(width/len(centroids))

    # loop over the color of each cluster
    for color in centroids:
        # plot the relative percentage of each cluster
        endX = startX + offset
        cv2.rectangle(img, (int(startX), 0), (int(endX), offset),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    return img


if __name__ == "__main__":
  # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    ap.add_argument("-c", "--clusters", required=True, type=int,
                    help="number of clusters")
    args = vars(ap.parse_args())

    # load the image and convert it from BGR to RGB
    image = cv2.imread(args["image"])
    height, width, channels = image.shape

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # reshape the image to be a list of pixels
    image_array = image.reshape((image.shape[0] * image.shape[1], 3))

    # cluster the pixel intensities
    clt = KMeans(n_clusters=args["clusters"])
    clt.fit(image_array)

    # create the color palette
    color_palette = plot_colors(clt.cluster_centers_, width)

    # creating the final image
    final_image = Image.new('RGB', (width, (height + 60)))
    color_palette_image = Image.fromarray(color_palette, 'RGB')
    image = Image.fromarray(image, 'RGB')

    final_image.paste(image, (0, 0))
    final_image.paste(color_palette_image, (0, height+5))

    # save and display the final image
    final_image.save('final_image.png')
    final_image.show()
