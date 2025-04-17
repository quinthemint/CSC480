from collections import deque
import heapq

# cardinal directions and their corresponding grid travel values
DIRECTIONS = [("N", -1, 0), ("S", 1, 0), ("W", 0, -1), ("E", 0, 1)]

# function that collects given start info and makes a set of all dirt through simple enumeration
def find_start_and_goals(grid):
    goals = set()
    start = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "@":
                start = (r, c)
            elif val == "*":
                goals.add((r, c))
    return start, goals

# finds new neighbors based on all valid directional moves from current position
def get_neighbors(r, c, grid, rows, cols):
    neighbors = []
    for action, dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            neighbors.append((action, nr, nc))
    return neighbors

# UCS
def uniform_cost_search(cols, rows, grid):
    # get start and dirt, instantiate visited set and heap structure
    start, goals = find_start_and_goals(grid)
    visited = set()
    heap = [(0, start, [], set())]  # (cost, position, path, cleaned)
    nodes_generated = 1
    nodes_expanded = 0

    while heap:

        # pop lowest cost node and skip states we've already visited
        cost, (r, c), path, cleaned = heapq.heappop(heap)
        state = (r, c, frozenset(cleaned))
        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        # if we have a new dirt, add it to cleaned set in state and add vacuum instruction to path
        if grid[r][c] == "*" and (r, c) not in cleaned:
            cleaned = set(cleaned)
            cleaned.add((r, c))
            path = path + ["V"]

        # cleaned set matching goal set means we're done, return output data
        if cleaned == goals:
            return path, nodes_generated, nodes_expanded

        # otherwise, we continue exploring each direction with get_neighbors,
        # incrementing cost on each new path
        for action, nr, nc in get_neighbors(r, c, grid, rows, cols):
            new_path = path + [action]
            heapq.heappush(heap, (cost + 1, (nr, nc), new_path, cleaned))
            nodes_generated += 1

    return [], nodes_generated, nodes_expanded

# DFS
def depth_first_search(cols, rows, grid):
    # get start and dirt, instantiate visited set and stack structure
    start, goals = find_start_and_goals(grid)
    visited = set()
    stack = [(start, [], set())] # position, path, cleaned
    nodes_generated = 1
    nodes_expanded = 0

    while stack:
        # pop from stack, LIFO. Still check to avoid already visited nodes
        (r, c), path, cleaned = stack.pop()
        state = (r, c, frozenset(cleaned))
        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        # if we have a new dirt, add it to cleaned set in state and add vacuum instruction to path
        if grid[r][c] == "*" and (r, c) not in cleaned:
            cleaned = set(cleaned)
            cleaned.add((r, c))
            path = path + ["V"]

        # cleaned set matching goal set means we're done, return output data
        if cleaned == goals:
            return path, nodes_generated, nodes_expanded

        # otherwise, we continue exploring each direction with get_neighbors,
        # appending new paths to the front of the stack to be explored first
        for action, nr, nc in get_neighbors(r, c, grid, rows, cols):
            new_path = path + [action]
            stack.append(((nr, nc), new_path, cleaned))
            nodes_generated += 1

    return [], nodes_generated, nodes_expanded
