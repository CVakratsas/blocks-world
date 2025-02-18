import os
import sys
import time

from blocks_world.bfs import bfs_solve
from blocks_world.dfs import dfs_solve
from blocks_world.heuristic_search import a_star_search, misplaced_blocks_heuristic, distance_to_goal_heuristic, \
    best_first_search
from blocks_world.problem_parser import print_data, extract_state, parse_problem
from blocks_world.utils import save_solution, solve_with_timeout, TimeoutException


def run_best_first(state, goal):
    return best_first_search(state, goal, misplaced_blocks_heuristic)


def run_a_star(state, goal):
    return a_star_search(state, goal, distance_to_goal_heuristic)


def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <algorithm> <input_file> <output_file>")
        sys.exit(1)

    algorithm = sys.argv[1].lower()  # 'bfs', 'dfs', 'best', or 'astar'
    input_file_name = sys.argv[2]  # Input file name
    output_file = sys.argv[3]  # Output file name
    input_file_path = f"./data/problems/{input_file_name}"  # Full path to input file
    output_file_path = f"./data/solutions/{output_file}.txt"  # Output file path

    # Check if the input file exists
    if not os.path.exists(input_file_path):
        print(f"Error: Input file {input_file_path} does not exist.")
        sys.exit(1)

    # Parse the problem and extract states
    print(f"Parsing problem from {input_file_path}...")
    parsed_data = parse_problem(input_file_path)
    initial_state = extract_state(parsed_data["initial_state"])
    goal_state = extract_state(parsed_data["goal_state"])

    # Select the algorithm
    if algorithm == "bfs":
        solve_function = bfs_solve
    elif algorithm == "dfs":
        solve_function = dfs_solve
    elif algorithm == "best":
        solve_function = run_best_first  # ✅ Use named function instead of lambda
    elif algorithm == "astar":
        solve_function = run_a_star  # ✅ Use named function instead of lambda
    else:
        print(f"Algorithm {algorithm} is not implemented.")
        sys.exit(1)

    # Solve with timeout
    try:
        start_time = time.time()
        solution, nodes_explored = solve_with_timeout(solve_function, (initial_state, goal_state), timeout=60)
        end_time = time.time()
        elapsed_time = end_time - start_time

        #  Save the solution to the output file
        if solution:
            print(f"Solution Length: {len(solution)} moves")
            print(f"Saving to {output_file_path}")
            save_solution(output_file_path, solution)
            print(f"Nodes Explored: {nodes_explored}")
            print(f"Time Taken: {elapsed_time:.4f} seconds")
        else:
            print("No solution found.")

    except TimeoutException as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
