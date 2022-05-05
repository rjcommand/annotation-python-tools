import pandas as pd
import cv2
import os
import glob
import numpy as np


# Define a function to load the annotation data .csv file for a desired transect
def load_data(data_path):
    # Get a list of csv files in the data_path directory
    file_path = glob.glob(data_path + str("*.csv"))

    # Get a list of files in the directory
    file_names = []
    for f in file_path:
        file_names.append(os.path.split(f)[1])

    file_names = pd.DataFrame(dict(file_path=file_path,
                                   files=file_names))
    file_names['transect_name'] = file_names['files'].str.split('_').str[:2].str.join('_')

    # Select a transect
    print(file_names['transect_name'])
    transect_id = input("Enter one of the above:   ")
    # while True:
    #   try:
    #       transect_id = input("Enter one of the above:   ")
    #       if transect_id not in file_names['transect_name']:
    #          print('Please enter a valid transect')
    #      else:
    #         break
    # except ValueError:
    #     print("Please enter in a correct format (CON_NUM)")

    # while True:
    #    if transect_id not in file_names['transect_name']:
    #        print("Nope, try again :)   :")
    #        print(file_names['transect_name'])
    #        transect_id = input("Enter one of the above:   ")
    #    break
    # Get the path to the corresponding .csv file
    csv_file = list(file_names.file_path[file_names.transect_name.str.contains(transect_id)])[0]
    return pd.read_csv(csv_file), transect_id


# Function to get a list of images that have annotations
def list_annotated_images(image_path, transect_id, transect_data):
    # Get a list of image files in the given transect directory
    # images = glob.glob(image_path + transect_id + "*.jpg")

    # Get the list of annotated images
    # Create empty lists
    annotated_image_path = []
    annotated_image_name = []
    # For each unique file name in the transect data frame
    for f in pd.unique(transect_data.filename):
        # Create a path to the corresponding file in the image folder
        img = os.path.join(image_path, transect_id, f)
        # If the image exists, add its name and path to the respective lists
        if os.path.isfile(img):
            annotated_image_path.append(img)
            annotated_image_name.append(os.path.split(img)[1])

    return annotated_image_name


# Function to extract the rois from each image in the transect based on the annotations in the .csv
def extract_rois(image_name, image_path, transect_data, transect_id):
    # Subset the annotation data frame to include only the given file
    data = transect_data[transect_data.filename.str.contains(image_name)]

    # Find the path to the image
    img_path = os.path.join(image_path, transect_id, image_name)

    # Read in the image
    img = cv2.imread(img_path, 1)

    # Get the x and y coordinates for each annotation (points and rectangles)
    df1 = data[["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"]]

    # Convert to numpy array
    arr = df1.to_numpy()

    # Get the labels associated with each annotation
    labels = data[["label_name"]]
    # Convert to numpy array
    lab_arr = labels.to_numpy()

    # Load the image
    original = img.copy()

    img_name = os.path.splitext(image_name)[0]
    extracted_dir = os.path.join(image_path, str(transect_id + '_extracted'))
    if not os.path.exists(extracted_dir):
        os.mkdir(extracted_dir)

    empty_rois = []
    roi_number = 0
    # loop through each coordinate pair in arr
    for item in range(len(arr)):
        # cv2.drawMarker(img, (int(arr[item][0]), int(arr[item][1])),(0,0,255),
        # markerSize=40, thickness=2, line_type=cv2.LINE_AA)
        if np.isnan(arr[item][2]):
            cv2.rectangle(img, (int(arr[item][0] - 200), int(arr[item][1] - 200)),
                          (int(arr[item][0] + 200), int(arr[item][1] + 200)), color=(0, 0, 255), thickness=4)
            # cv2.putText(img, text = str(lab_arr[item][0]), org = (int(arr[item][0]+80), int(arr[item][1]-80)),
            #           fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.8, color = (0, 0, 255),
            #          thickness = 2, lineType = cv2.LINE_AA)
            x, y, w, h = int(arr[item][0] - 200), int(arr[item][1] - 200), 400, 400
            roi = original[y:y + h, x:x + h]

        # If it is a rectangle annotation
        if not np.isnan(arr[item][2]):
            x_min = int(min(arr[item][0], arr[item][2], arr[item][4], arr[item][6]))
            x_max = int(max(arr[item][0], arr[item][2], arr[item][4], arr[item][6]))
            y_min = int(min(arr[item][1], arr[item][3], arr[item][5], arr[item][7]))
            y_max = int(max(arr[item][1], arr[item][3], arr[item][5], arr[item][7]))
            cv2.rectangle(img, (x_min, y_max),
                          (x_max, y_min), color=(0, 0, 255), thickness=4)
            # cv2.putText(img, text = str(lab_arr[item][0]), org = (int(arr[item][0]+80), int(arr[item][1]-80)),
            #           fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.8, color = (0, 0, 255),
            #          thickness = 2, lineType = cv2.LINE_AA)
            x, y, w, h = int(x_min), int(y_min), int(x_max), int(y_max)
            roi = original[y:h, x:w]

        # Create extracted taxa directories if needed
        extracted_dir_taxa = os.path.join(extracted_dir, str(lab_arr[item][0]))
        if not os.path.exists(extracted_dir_taxa):
            os.mkdir(extracted_dir_taxa)

        # Create a unique file name
        roi_file_name = img_name + '_' + str(lab_arr[item][0]) + '_{}.png'.format(roi_number)

        # Create a path to the file in the appropriate extracted directory for the taxa
        write_path = os.path.join(extracted_dir_taxa, roi_file_name)

        # Check if the ROI exists. If it doesn't, add it to the list of empty ROI
        # Also set write_path to false so it gets skipped but doesn't disrupt the loop
        if roi.size == 0:
            empty_rois.append(roi_file_name)
            write_path = False
        print(write_path)
        # Check if write path is False; if it is, continue the loop but don't try to write the image file.
        # If it's not False, write the image file
        if not write_path:
            continue
        else:
            cv2.imwrite(write_path, roi)

        roi_number += 1
        # time.sleep(-time.time() % 0.5)

    marked_dir = os.path.join(image_path, str(transect_id + '_marked'))
    if not os.path.exists(marked_dir):
        os.mkdir(marked_dir)
    write_marked = os.path.join(marked_dir, str('MARKED_' + image_name))
    cv2.imwrite(write_marked, img)
    return empty_rois


def main():
    # Path to the directory containing the .csv files with the annotation coordinates
    data_path = 'C:\\Users\\COMMANDR\\Documents\\ID Guide\\ID Guide\\data\\processed\\ROI_all\\*'

    # Load the annotation data csv file
    # Save the data as transect_data (pandas data frame)
    # Save the user input transect id as transect_id
    transect_data, transect_id = load_data(data_path=data_path)

    # Path to the directory containing all the annotated image directories (by transect, i.e. CON_014/, CON_015/ etc.)
    image_path = 'C:\\Users\\COMMANDR\\Documents\\ID Guide\\Images\\full_images'

    # Get a list of images in the image_path\transect_id directory that have been annotated
    # Save the result as annotated_images (list)
    annotated_images = list_annotated_images(image_path=image_path, transect_id=transect_id,
                                             transect_data=transect_data)

    [extract_rois(image_name, image_path, transect_data, transect_id) for image_name in annotated_images]


if __name__ == "__main__":
    main()
