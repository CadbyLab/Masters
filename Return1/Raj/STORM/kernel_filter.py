import STORM_Samurai as sam
import numpy as np
import matplotlib.pyplot as plt

array = sam.loadtiffs("/Users/RajSeehra/University/Masters/Semester 2/Teaching_python-master/Week 2/Data/640.tif")


def kernel_filter(data, matrix):
    image = data
    kernel = np.asarray(matrix)
    if sum(sum(kernel)) != 1:       # Quick check to ensure the kernel matrix is within parameters.
        print("Error, this matrix's summation value is not equal to 1. This can change the final image.")

    edge_cover = (kernel.shape[0] - 1) // 2

    # adds an edge to allow pixels at the border to be filtered too.
    # ??? should i change the zeros to replicate the edge pixels?
    bordered_image = np.zeros((data.shape[0]+2*edge_cover, data.shape[1]+2*edge_cover))
    # makes the central pixels the ones from the image, leaving surrounding as zeroes.
    bordered_image[edge_cover:bordered_image.shape[0]-edge_cover, edge_cover: bordered_image.shape[1]-edge_cover] = image
    # Our blank canvas below.
    processed_image = np.zeros((bordered_image.shape[0], bordered_image.shape[1]))

    # Iterates the x and y positions.
    for x in range(edge_cover, bordered_image.shape[1]-edge_cover):
        for y in range(edge_cover, bordered_image.shape[0]-edge_cover):
            kernel_region = bordered_image[y-edge_cover:y+edge_cover+1, x-edge_cover:x+edge_cover+1]
            k = (kernel * kernel_region).sum()
            processed_image[y,x] = k
    processed_image = processed_image[edge_cover:processed_image.shape[0]-edge_cover, edge_cover:processed_image.shape[1]-edge_cover]
    return(processed_image)


matrix = np.asarray([(-1, 0, -1), (0, 5, 0), (-1, 0, -1)])

# Data input is a single image frame and the matrix "? multipliers"
img = kernel_filter(array[:,:,0], matrix)


plt.subplot(121)
plt.imshow(array[:,:,0])
plt.title("Original")
plt.subplot(122)
plt.imshow(img)
plt.title("After")
plt.show()