import multiprocessing
import signal
import sys

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
        if current not in moves:
            raise KeyError(f"State {current} not found in moves dictionary.")

        path.append(moves[current])  # Add the move that led to the current state
        current = prev[current]  # Move to the predecessor
    path.reverse()  # Reverse to get the correct order
    return path


class TimeoutException(Exception):
    pass

# ✅ Windows Function to Run the Solver
def solve_worker(solve_function, args, queue):
    """Standalone function to run the solver inside a separate process."""
    try:
        result = solve_function(*args)
        queue.put(result)  # Send result back through the queue
    except Exception as e:
        queue.put(e)


def solve_with_timeout(solve_function, args, timeout=60):
    """
    Run a function with a timeout.
    :param solve_function: Function to run (e.g., bfs_solve or dfs_solve).
    :param args: Arguments to pass to the function.
    :param timeout: Maximum time allowed (in seconds).
    :return: Result of the function if completed within timeout, otherwise None.
    """
    if sys.platform.startswith("win"):  # Windows uses multiprocessing
        return solve_with_timeout_windows(solve_function, args, timeout)
    else:  # Linux/macOS uses signals
        return solve_with_timeout_unix(solve_function, args, timeout)


# ✅ Linux/macOS Version (Using `signal`)
def solve_with_timeout_unix(solve_function, args, timeout=60):
    """UNIX-based timeout handling using signal."""
    def timeout_handler(signum, frame):
        raise TimeoutException("Execution exceeded the time limit of 60 seconds.")

    signal.signal(signal.SIGALRM, timeout_handler)  # Set timeout handler
    signal.alarm(timeout)  # Start countdown

    try:
        result = solve_function(*args)  # Run the solver
        signal.alarm(0)  # Cancel alarm if execution finishes in time
        return result
    except TimeoutException:
        raise TimeoutException(f"Execution exceeded the time limit of {timeout} seconds.")


# ✅ Windows Version (Using `multiprocessing`)
def solve_with_timeout_windows(solve_function, args, timeout=60):
    """Windows timeout handling using multiprocessing (forcefully kills process after timeout)."""
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=solve_worker, args=(solve_function, args, queue))

    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()  # Kill the process if it exceeds timeout
        process.join()
        raise TimeoutException(f"Execution exceeded the time limit of {timeout} seconds.")

    if not queue.empty():
        result = queue.get()
        if isinstance(result, Exception):
            raise result  # Re-raise error if function crashed
        return result

    raise TimeoutException("No result returned from the solve function.")


# ✅ Main Timeout Function (Auto-selects Windows or UNIX version)
def solve_with_timeout(solve_function, args, timeout=60):
    """Run a function with a timeout."""
    if sys.platform.startswith("win"):
        return solve_with_timeout_windows(solve_function, args, timeout)
    else:
        return solve_with_timeout_unix(solve_function, args, timeout)