# Splits images from input_images into objects and saves them to output_images

import os
import sys
import numpy as np
from PIL import Image

def split_objects(block_width, block_height):
    pass

def dfs_graph(node, graph_np, visited, color, block_width, block_height):
    if visited[node["index"]]:
        return
    visited[node["index"]] = True
    graph_np[node["y"]: node["y"] + block_height, node["x"]: node["x"] + block_width] = color

    for edge in node["edges"]:
        dfs(edge, graph_np, visited, color)


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
            np.any(image_np[y: y + 32, x, 3] == 255) and 
            np.any(image_np[y: y + 32, x - 1, 3] == 255)):
                ed_index = node["index"] - 1
                if nodes[ed_index]:
                    node["edges"] = np.append(node["edges"], nodes[ed_index])
        
        # Check right border
        if x < width - 32:
            if np.any(image_np[y: y + 32, x + 31, 3] == 255) and np.any(image_np[y: y + 32, x + 32, 3] == 255):
                ed_index = node["index"] + 1
                if nodes[ed_index]:
                    node["edges"] = np.append(node["edges"], nodes[ed_index])


def main():
    input_folder = "../input_images/"
    output_folder = "../output_images/"
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
    
            image = Image.open(input_folder + filename)
            width, height = image.size
            image_np = np.array(image)

            print("{} size in pixels: {} x {}".format(filename, width, height))
            splited_folder = output_folder + filename[:-4] + "/"
            if not os.path.exists(splited_folder):
                os.makedirs(splited_folder)
            
            nodes = create_nodes(image_np, block_width, block_height)
            
            # Create edges
            nodes = create_edges(nodes, image_np, block_width, block_height)
            
            
            # Create edges
            
            # Make image of graph with dfs
            graph = Image.new("RGBA", (width, height))
            graph_np = np.array(graph)
            visited = np.zeros((width // 32) * (height // 32), dtype=bool)
            for node in nodes:
                if not node:
                    continue
                color = np.random.randint(0, 255, 4)
                color[3] = 255
                dfs(node, graph_np, visited, color)
            graph = Image.fromarray(graph_np)
            graph.save(directory + "graph_" + filename)
            
            # Build images of objects with bfs
            visited = np.zeros((width // 32) * (height // 32), dtype=bool)
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
                    obj_np[node["y"]: node["y"] + 32, node["x"]: node["x"] + 32] = image_np[node["y"]: node["y"] + 32, node["x"]: node["x"] + 32]
                    for edge in node["edges"]:
                        if not visited[edge["index"]]:
                            queue.append(edge)
                            visited[edge["index"]] = True
                obj = Image.fromarray(obj_np)
                obj.save(directory + str(node["index"]) + ".png")
            print("Objects separated for " + filename)

                    
            

if __name__ == '__main__':
    main()
