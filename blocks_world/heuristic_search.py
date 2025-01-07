import heapq

from blocks_world.graph import generate_neighbors
from blocks_world.utils import reconstruct_path

import heapq


def best_first_search(initial_state, goal_state, heuristic):
    """
    Best-First Search algorithm.
    :param initial_state: Initial BlockWorldState.
    :param goal_state: Goal BlockWorldState.
    :param heuristic: Heuristic function to guide the search.
    :return: Solution path and nodes explored.
    """
    frontier = []
    heapq.heappush(frontier, (heuristic(initial_state, goal_state), initial_state))
    explored = set()
    prev = {initial_state: None}  # Map to track the predecessor of each state
    moves = {initial_state: None}  # Map to track the move leading to each state
    nodes_explored = 0

    while frontier:
        # Pop the state with the lowest heuristic value
        _, current_state = heapq.heappop(frontier)
        nodes_explored += 1

        # Check if the goal state is reached
        if current_state == goal_state:
            return reconstruct_path(prev, moves, initial_state, current_state), nodes_explored

        explored.add(current_state)

        # Expand neighbors
        for neighbor in generate_neighbors(current_state):
            if neighbor not in explored:
                h_value = heuristic(neighbor, goal_state)
                heapq.heappush(frontier, (h_value, neighbor))
                prev[neighbor] = current_state  # Track the predecessor
                moves[neighbor] = neighbor.action  # Track the move leading to this state

    # If no solution is found
    return None, nodes_explored


def a_star_search(initial_state, goal_state, heuristic):
    """
    A* search algorithm.
    :param initial_state: Initial BlockWorldState.
    :param goal_state: Goal BlockWorldState.
    :param heuristic: Heuristic function to guide the search.
    :return: Solution path and nodes explored.
    """
    frontier = []  # Priority queue for A*
    heapq.heappush(frontier, (0, initial_state))  # Push (f, state)
    explored = set()
    nodes_explored = 0

    while frontier:
        _, current_state = heapq.heappop(frontier)
        nodes_explored += 1

        if current_state == goal_state:
            return reconstruct_path(current_state), nodes_explored

        explored.add(current_state)

        for child in generate_neighbors(current_state):
            if child not in explored:
                child.f = child.cost + heuristic(child, goal_state)
                heapq.heappush(frontier, (child.f, child))

    return None, nodes_explored


def misplaced_blocks_heuristic(state, goal_state):
    """
    Count the number of misplaced blocks compared to the goal state.
    :param state: Current BlockWorldState.
    :param goal_state: Goal BlockWorldState.
    :return: Number of misplaced blocks.
    """
    misplaced = 0
    for block, goal_block in goal_state.on.items():
        if state.on.get(block) != goal_block:
            misplaced += 1
    return misplaced


def distance_to_goal_heuristic(state, goal_state):
    """
    Compute the total number of moves required to place each block in its correct position.
    :param state: Current BlockWorldState.
    :param goal_state: Goal BlockWorldState.
    :return: Total estimated cost to reach the goal.
    """
    distance = 0
    for block, goal_block in goal_state.on.items():
        # If the block is not in the correct position
        current_pos = state.on.get(block, "TABLE")
        if current_pos != goal_block:
            distance += 1  # One move needed to fix the block
    return distance
