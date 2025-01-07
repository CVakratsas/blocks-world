import threading


def save_solution(file_path, solution):
    """
    Save the solution to a file in the specified format.
    """
    with open(file_path, "w") as f:
        for move in solution:
            f.write(f"{move}\n")


def reconstruct_path(prev, moves, start, end):
    """
    Reconstruct path from BFS by tracing back from the end node to the start node.
    :param prev: Dictionary mapping states to their predecessor states.
    :param moves: Dictionary mapping states to the moves that led to them.
    :param start: The starting state.
    :param end: The goal state.
    :return: List of moves leading from the start to the goal.
    """
    path = []
    current = end
    while current != start:
        path.append(moves[current])  # Add the move that led to the current state
        current = prev[current]  # Move to the predecessor
    path.reverse()  # Reverse to get the correct order
    return path


class TimeoutException(Exception):
    pass


def solve_with_timeout(solve_function, args, timeout=60):
    """
    Run a function with a timeout.
    :param solve_function: Function to run (e.g., bfs_solve or dfs_solve).
    :param args: Arguments to pass to the function.
    :param timeout: Maximum time allowed (in seconds).
    :return: Result of the function if completed within timeout, otherwise None.
    """
    result = {}

    def target():
        try:
            result["output"] = solve_function(*args)
        except Exception as e:
            result["error"] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        thread.join(0)
        raise TimeoutException("Execution exceeded the time limit of 60 seconds.")

    if "error" in result:
        raise result["error"]

    return result.get("output")  # Pass the full return value of solve_function

