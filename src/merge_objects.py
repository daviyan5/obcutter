# Merges the objects in input_images into a single image and saves it to output_images
import PIL
import os
import sys
import numpy as np


def merge_objects(rows, columns, spacing):
    input_folder = "../input_images/"
    if not os.path.exists(input_folder):
        print("Input folder does not exist")
        return
    output_folder = "../output_images/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    
    objs_array = np.empty((0), dtype=object)
    counter = 0
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            image = PIL.Image.open(input_folder + filename)
            image_np = np.array(image)
            objs_array.resize((counter + 1))
            objs_array[counter] = image_np
            counter += 1
    print("Number of objects: " + str(len(objs_array)))
    assert counter != 0, "No images found in input_images folder"
    assert len(objs_array) == counter, "Error: len(objs_array) != counter"

    if rows != 0 and columns != 0:
        if rows * columns != len(objs_array):
            print("ERROR: rows * columns != number of objects")
            return
        else:
            objs_array = objs_array.reshape(rows, columns)
    elif rows != 0:
        while(len(objs_array) % rows != 0):
            objs_array = np.append(objs_array, np.zeros((1, objs_array[0].shape[0], objs_array[0].shape[1]), dtype=object))
        objs_array = objs_array.reshape(len(objs_array) // rows, rows)
    elif columns != 0:
        while(len(objs_array) % columns != 0):
            objs_array = np.append(objs_array, np.zeros((1, objs_array[0].shape[0], objs_array[0].shape[1]), dtype=object))
        objs_array = objs_array.reshape(columns, len(objs_array) // columns)
    else:
        rows = int(np.sqrt(len(objs_array)))
        while(len(objs_array) % rows != 0):
            objs_array = np.append(objs_array, np.zeros((1, objs_array[0].shape[0], objs_array[0].shape[1]), dtype=object))
        objs_array = objs_array.reshape(rows, len(objs_array) // rows)

    row_size = max([objs_array[i][j].shape[0] for i in range(objs_array.shape[0]) for j in range(objs_array.shape[1])])
    column_size = max([objs_array[i][j].shape[1] for i in range(objs_array.shape[0]) for j in range(objs_array.shape[1])])
    merged_image = np.zeros((row_size * objs_array.shape[0] + spacing * (objs_array.shape[0] - 1), column_size * objs_array.shape[1] + spacing * (objs_array.shape[1] - 1), 4), dtype=np.uint8)
    for i in range(objs_array.shape[0]):
        for j in range(objs_array.shape[1]):
            merged_image[i * (row_size + spacing):i * (row_size + spacing) + objs_array[i][j].shape[0], j * (column_size + spacing):j * (column_size + spacing) + objs_array[i][j].shape[1]] = objs_array[i][j]

    merged_image = PIL.Image.fromarray(merged_image)
    merged_image.save(output_folder + "merged.png")
    print("Merged image saved to " + output_folder + "merged.png")

            