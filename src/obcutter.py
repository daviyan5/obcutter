# Main program for the OBCutter application
import os
import sys
import click
from split_objects import split_objects
from merge_objects import merge_objects

version = "0.1.0"
@click.command()
@click.option('--split', '-s', 'operation',flag_value='split', help='Split the file into multiple files')
@click.option('--width', '-w', default=1, help='Width of the object block to be splitted in pixels, default 1')
@click.option('--height', '-h', default=1, help='Height of the object block to be splitted in pixels, default 1')
@click.option('--bounding-box', '-b',is_flag=True, default=False, help='Bounds the png image to the bounding box of the pixels')
@click.option('--graph', '-g',is_flag=True, default=False, help='Draws the graph of the objects')

@click.option('--merge', '-m', 'operation',flag_value='merge', help='Merge the files into a single file')
@click.option('--rows', '-r', default=0, help='Number of rows in the merge file, 0 for auto')
@click.option('--columns', '-c', default=0, help='Number of columns in the merge file, 0 for auto')
@click.option('--spacing', '-p', default=1, help='Spacing between the objects in pixels, default 1')

def main(operation, width, height, bounding_box, graph, rows, columns, spacing):
    # Deals with the command line arguments
    
    print("OBcutter v", version)
    if operation == 'split':
        print("Splitting image into objects")
        print("\tObject block -> width: {} pixels, height: {} pixels".format(width, height))
        print("\tBounding box -> {}".format("on" if bounding_box else "off"))
        print("\tGraph -> {}".format("on" if graph else "off"))
        print("--------------------------------\n")
        split_objects(width, height, bounding_box, graph)
        
    elif operation == 'merge':
        print("Merging objects into image")
        print("\tMerge image -> rows: {}, columns: {}".format(rows if rows > 0 else "auto", columns if columns > 0 else "auto"))
        print("\tSpacing -> {} pixels".format(spacing))
        print("--------------------------------\n")
        merge_objects(rows, columns, spacing)

    
    
    


if __name__ == "__main__":
    main()