import os
from skimage.color.colorconv import rgb2gray
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage import morphology
from skimage.measure import label, regionprops

def handle_image(file_name):
    image_data = plt.imread(os.path.join('img', file_name))

    grayscale_image = rgb2gray(image_data)
    threshold_value = threshold_otsu(grayscale_image)
    binary_image = grayscale_image < threshold_value
    eroded_image = morphology.binary_erosion(binary_image)
    dilated_image = morphology.binary_dilation(eroded_image)
    labeled_image = label(dilated_image)
    cropped_labeled_image = labeled_image[50:-50, 50:-50]
    regions = regionprops(cropped_labeled_image)

    count = 0
    for region in regions:
        # elongation of the figure
        if region.eccentricity > 0.99 and region.equivalent_diameter > 170:
            count += 1

    print(f'в {file_name} {count} карандашей')
    return count

def main():
    image_files = os.listdir(path='img')
    total_count = 0

    for file_name in image_files:
        total_count += handle_image(file_name)

    print("Total count:", total_count)

main()

