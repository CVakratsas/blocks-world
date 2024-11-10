from blocks_world.problem_parser import parse_problem
from blocks_world.bfs import bfs_solve
from blocks_world.heuristic_search import best_first_search, a_star_search
from blocks_world.utils import save_solution

def solve_problem(algorithm, input_file, output_file):
    # Parse the problem file
    initial_state, goal_state = parse_problem(input_file)

    # Select algorithm and solve
    if algorithm == "bfs":
        solution = bfs_solve(initial_state, goal_state)
    elif algorithm == "best":
        solution = best_first_search(initial_state, goal_state)
    elif algorithm == "astar":
        solution = a_star_search(initial_state, goal_state)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    # Save the solution to the output file
    save_solution(output_file, solution)
