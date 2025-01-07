from blocks_world.graph import generate_neighbors
from blocks_world.utils import reconstruct_path


def dfs_solve(initial_state, goal_state):
    """
    Solve the Blocks World problem using DFS.
    :param initial_state: BlockWorldState object representing the initial state.
    :param goal_state: BlockWorldState object representing the goal state.
    :return: A tuple of (solution path as a list of moves, number of nodes explored).
    """
    frontier = [initial_state]  # Stack for DFS
    visited = set()  # Track visited states
    prev = {initial_state: None}  # Map to reconstruct the path
    moves = {initial_state: None}  # Store the action leading to each state
    nodes_explored = 0

    while frontier:
        # Pop the last state (LIFO behavior)
        current_state = frontier.pop()
        nodes_explored += 1

        # Check if the goal is reached
        if current_state == goal_state:
            print("Goal state matched!")
            solution_path = reconstruct_path(prev, moves, initial_state, current_state)
            return solution_path, nodes_explored

        visited.add(current_state)

        # Expand neighbors
        for neighbor in generate_neighbors(current_state):
            if neighbor not in visited and neighbor not in frontier:
                frontier.append(neighbor)  # Push to the stack
                prev[neighbor] = current_state  # Store the predecessor
                moves[neighbor] = neighbor.action  # Store the action leading to this state

    return None, nodes_explored
