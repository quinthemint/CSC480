import sys
from search_algorithms import uniform_cost_search, depth_first_search

# function to extract the number columns and rows, and the actual grid 
def parse_world(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    cols = int(lines[0])
    rows = int(lines[1])
    grid = lines[2:]
    return cols, rows, grid

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [algorithm] [world-file]")
        sys.exit(1)

    # get the command line args
    algo = sys.argv[1]
    filename = sys.argv[2]

    # extract world data
    cols, rows, grid = parse_world(filename)

    # check for algorithm type, then get output for printing
    if algo == "uniform-cost":
        actions, nodes_generated, nodes_expanded = uniform_cost_search(cols, rows, grid)
    elif algo == "depth-first":
        actions, nodes_generated, nodes_expanded = depth_first_search(cols, rows, grid)
    else:
        print("Unknown algorithm:", algo)
        sys.exit(1)

    # print actions and node data
    for action in actions:
        print(action)
    print(f"{nodes_generated} nodes generated")
    print(f"{nodes_expanded} nodes expanded")
