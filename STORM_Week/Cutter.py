import general as genr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def square_area(img, xcoords, ycoords, size=11):
    square_size = int(size)
    if square_size%2 == 0:
        print("None odd number hence cutout is flawed to one side.")
        print("Size value has been altered by adding 1 to it.")
        square_size = square_size +1
    # Assign intial coords for image
    xcoordmin = xcoords - int(square_size//2)
    xcoordmax = xcoords + int(square_size//2)+1
    ycoordmin = ycoords - int(square_size//2)
    ycoordmax = ycoords + int(square_size//2)+1

    # check no negative numbers, correct the squares position if at an edge.
    if xcoordmin < 0:
        xcoordmin = 0
        xcoordmax = xcoordmin + square_size
    if xcoordmax > img.shape[1]:
        xcoordmax = img.shape[1]
        xcoordmin = xcoordmax - square_size
    if ycoordmin < 0:
        ycoordmin = 0
        ycoordmax = ycoordmin + square_size
    if ycoordmax > img.shape[0]:
        ycoordmax = img.shape[0]
        ycoordmin = ycoordmax - square_size

    # Plotting the area.
    return img[ycoordmin:ycoordmax, xcoordmin:xcoordmax]


def area_filter(data, lower_bound=0, upper_bound=5):
    data = data[data['area'] >= lower_bound]  # at area >0 with std 5 can pick up all appropriate intensities.
    data = data[data['area'] <= upper_bound]
    return data


### IMPORT ###
data = pd.read_csv(
    "/Users/RajSeehra/University/Masters/Semester 2/test folder/storm_output_data/panda_data_8_2020-04-15 16:32:28.277292_.csv")

### BOUNDING ###
# Remove the excess first column, an artifact from exporting a csv.
data = data.drop('Unnamed: 0', axis=1)
data = data.reset_index()

# Filters the data set by the area to remove files that are above or below the thresholding limits.
data = area_filter(data, 1, 2)
data = data.reset_index()
data = data.drop('level_0', axis=1)
data = data.drop('index', axis=1)



### PROCESSING ###
# Generate a file list from the data. As there are repeated filenames this compares the next file name to the current
# and if they are different adds the next filename to the list.
file_list = [data["file_name"][0]]
for i in range(0, data.shape[0]-1):
    if data["file_name"][i+1] == data["file_name"][i]:
        continue
    else:
        file_list.append(data["file_name"][i+1])

# Create an empty array to add the data to.
cutouts = np.zeros([11, 11, data.shape[0]])
cutout_dataframe = pd.DataFrame(columns=['frame', 'X', 'Y', 'filename'])

for i in range(0, len(file_list)):
    img = genr.load_img(file_list[i])   # loads in the file
    print(file_list[i])
    for j in range(0, data.shape[0]):
        if data["file_name"][j] == file_list[i]:
            y = data["centroid-0"][j]
            x = data["centroid-1"][j]
            print(x, y)

            cutouts[:, :, j] = square_area(img, x, y)
            cutout_current = pd.DataFrame({'frame': [j], 'X': [x],'Y': [y], 'filename': [file_list[i]]})
            cutout_dataframe = pd.concat([cutout_dataframe, cutout_current], axis=0)

# Currently Data is offset by the rounding issue with the localisation. Data needs to be adjusted to match.

img2 = genr.load_img("/Users/RajSeehra/University/Masters/Semester 2/test folder/00008.tif")
plt.subplot(121)
plt.imshow(cutouts[:,:,4])
plt.subplot(122)
plt.imshow(img2)
plt.show()