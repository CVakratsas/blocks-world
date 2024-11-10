import sys
from blocks_world.solver import solve_problem

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <algorithm> <input_file> <output_file>")
        sys.exit(1)

    algorithm = sys.argv[1]  # 'bfs', 'best', or 'astar'
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    # Solve the problem
    solve_problem(algorithm, input_file, output_file)


if __name__ == "__main__":
    main()
