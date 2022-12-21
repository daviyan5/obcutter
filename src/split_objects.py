# Splits images from input_images into objects and saves them to output_images

import os
import sys
import numpy as np
from PIL import Image

# Set recursion limit to 10000
sys.setrecursionlimit(10000)


def dfs_graph(node, graph_np, visited, color, block_width, block_height):
    if visited[node["index"]]:
        return
    visited[node["index"]] = True
    graph_np[node["y"]: node["y"] + block_height, node["x"]: node["x"] + block_width] = color

    for edge in node["edges"]:
        dfs_graph(edge, graph_np, visited, color, block_width, block_height)


def create_nodes(image_np, block_width, block_height):
    width, height = image_np.shape[:2]
    
    num_blocks_x = width // block_width
    num_blocks_y = height // block_height
    nodes = np.empty(num_blocks_x * num_blocks_y, dtype=object)

    for i in range(0, height, block_height):
        for j in range(0, width, block_width):

            if np.any(image_np[i: i + block_height, j: j + block_width, 3] == 255):
                
                index = (i // block_height) * num_blocks_x + j // block_width
                node = {"x": j, "y": i, "index": index, "edges": np.empty(0, dtype=object)}
                nodes[index] = node

    return nodes

def create_edges(nodes, image_np, num_blocks_x, num_blocks_y, block_width, block_height):
    width, height = image_np.shape[:2]
    for node in nodes:
        if not node:
            continue

        x = node["x"]
        y = node["y"]

        # Check up border
        if (y > 0 and 
            np.any(image_np[y, x: x + block_width, 3] == 255) and 
            np.any(image_np[y - 1, x: x + block_width, 3] == 255)):

            ed_index = node["index"] - num_blocks_x
            if nodes[ed_index]:
                node["edges"] = np.append(node["edges"], nodes[ed_index])
        
        # Check down border
        if (y < height - block_height and 
            np.any(image_np[y + block_height - 1, x: x + block_width, 3] == 255) and 
            np.any(image_np[y + block_height, x: x + block_width, 3] == 255)):

            ed_index = node["index"] + num_blocks_x
            if nodes[ed_index]:
                node["edges"] = np.append(node["edges"], nodes[ed_index])

        # Check left border
        if (x > 0 and 
            np.any(image_np[y: y + block_height, x, 3] == 255) and 
            np.any(image_np[y: y + block_height, x - 1, 3] == 255)):

            ed_index = node["index"] - 1
            if nodes[ed_index]:
                node["edges"] = np.append(node["edges"], nodes[ed_index])
        
        # Check right border
        if (x < width - 32 and 
            np.any(image_np[y: y + block_height, x + block_width - 1, 3] == 255) and 
            np.any(image_np[y: y + block_height, x + block_width, 3] == 255)):

            ed_index = node["index"] + 1
            if nodes[ed_index]:
                node["edges"] = np.append(node["edges"], nodes[ed_index])
    return nodes

def create_graph(nodes, width, height, block_width, block_height, splited_folder, filename):
    graph = Image.new("RGBA", (width, height))
    graph_np = np.array(graph)
    visited = np.zeros((width // block_width) * (height // block_height), dtype=bool)
    for node in nodes:
        if not node:
            continue
        color = np.random.randint(0, 255, 4)
        color[3] = 255
        dfs_graph(node, graph_np, visited, color, block_width, block_height)
    graph = Image.fromarray(graph_np)
    graph.save(splited_folder + "graph_" + filename)

def bound_box(im):
    pixdata = im.load()

    width, height = im.size
    minx = width
    miny = height
    maxx = 0
    maxy = 0

    for y in range(height):
        for x in range(width):
            if pixdata[x, y][3] == 255:
                minx = min(minx, x)
                miny = min(miny, y)
                maxx = max(maxx, x)
                maxy = max(maxy, y)

    im2 = im.crop((minx, miny, maxx + 1, maxy + 1))
    return im2

def build_objects(nodes, image_np, width, height, block_width, block_height, splited_folder, bounding_box):
    visited = np.zeros((width // block_width) * (height // block_height), dtype=bool)
    for node in nodes:
        if not node:
            continue
        if visited[node["index"]]:
            continue
        queue = [node]
        visited[node["index"]] = True
        obj = Image.new("RGBA", (width, height))
        obj_np = np.array(obj)
        while queue:
            node = queue.pop(0)
            obj_np[node["y"]: node["y"] + block_height, node["x"]: node["x"] + block_width] = image_np[node["y"]: node["y"] + block_height, node["x"]: node["x"] + block_width]
            for edge in node["edges"]:
                if not visited[edge["index"]]:
                    queue.append(edge)
                    visited[edge["index"]] = True
        obj = Image.fromarray(obj_np)
        if bounding_box:
            obj = bound_box(obj)
        obj.save(splited_folder + str(node["index"]) + ".png")

def clear_output_folder(output_folder):
    print("{} FOLDER IS GOING TO BE CLEARED".format(output_folder))
    print("ARE YOU SURE YOU WANT TO CONTINUE? (y/n)")
    if input() == "y":
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        return 0
        
    else:
        return 1
    
def split_objects(block_width, block_height, bounding_box, graph):
    input_folder = "../input_images/"
    if not os.path.exists(input_folder):
        print("Input folder does not exist")
        return
    output_folder = "../output_images/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
    
            image = Image.open(input_folder + filename)
            width, height = image.size

            image_np = np.array(image)

            if width % block_width != 0 or height % block_height != 0:
                
                print("WARNING: Image size is not divisible by block size, splitting might not work properly\n")
                width = width - width % block_width
                height = height - height % block_height
                image_np = image_np[:height, :width]
                

            num_blocks_x = width // block_width
            num_blocks_y = height // block_height

            print("{} size in pixels: {} x {}".format(filename, width, height))
            splited_folder = output_folder + filename[:-4] + "/"
            if not os.path.exists(splited_folder):
                os.makedirs(splited_folder)
            else:
                # Clear
                code = clear_output_folder(splited_folder)
                print("--------------------------------\n")
                if code == 1:
                    return
            
            nodes = create_nodes(image_np, block_width, block_height)
            
            # Create edges
            nodes = create_edges(nodes, image_np, num_blocks_x, num_blocks_y, block_width, block_height)
            
            # Build image graph
            if graph:
                create_graph(nodes, width, height, block_width, block_height, splited_folder, filename)
                
            # Build images of objects with bfs
            build_objects(nodes, image_np, width, height, block_width, block_height, splited_folder, bounding_box)
            
            print("Objects separated for " + filename)

    print("Splitting finished")

