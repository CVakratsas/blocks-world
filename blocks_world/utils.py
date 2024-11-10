def save_solution(file_path, solution):
    """
    Save the solution to a file in the specified format.
    """
    with open(file_path, "w") as f:
        for move in solution:
            f.write(f"{move}\n")

def reconstruct_path(prev, start, end):
    """
    Reconstruct path from BFS or A* by tracing back from the end node to the start node.
    """
    path = []
    at = end
    while at is not None:
        path.append(at)
        at = prev[at]
    path.reverse()
    return path if path[0] == start else []
