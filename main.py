import sys

from blocks_world.graph import generate_neighbors, build_graph, print_graph
from blocks_world.solver import solve_problem
from blocks_world.problem_parser import print_data, extract_state, parse_problem
from blocks_world.state import move


def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <algorithm> <input_file> <output_file>")
        sys.exit(1)

    algorithm = sys.argv[1]  # 'bfs', 'best', or 'astar'
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    # print_data(input_file, output_file)
    #
    # # Solve the problem
    # solve_problem(algorithm, input_file, output_file)
    #
    # # Parse the problem
    # parsed_data = parse_problem(input_file)
    #
    # # Extract initial state node
    # print("Initial State Node (BlockWorldState):")
    # initial_state_node = extract_state(parsed_data["initial_state"])
    # print(initial_state_node)
    #
    # # Extract goal state node
    # goal_state_node = extract_state(parsed_data["goal_state"])
    # print("Goal State Node (BlockWorldState):")
    # print(goal_state_node)

    # Step 1: Parse the problem and extract the initial state
    parsed_data = parse_problem(input_file)
    initial_state_node = extract_state(parsed_data["initial_state"])
    print("Initial State Node (BlockWorldState):")
    print(initial_state_node)

    # Step 3: Test the generate_neighbors function
    print("\nTesting generate_neighbors function:")
    neighbors = generate_neighbors(initial_state_node)
    print(f"Generated {len(neighbors)} neighbor states:")
    for i, neighbor in enumerate(neighbors, 1):
        print(f"Neighbor {i}: {neighbor}")

    # Step 4: Test the build_graph function
    print("\nTesting build_graph function:")
    graph = build_graph(initial_state_node)

    # Print the graph in a readable way
    print_graph(graph)


if __name__ == "__main__":
    main()

# # Example usage
# if __name__ == "__main__":
#     # Number of vertices in the graph
#     V = 5
#
#     # Adjacency list representation of the graph
#     adj = [[] for _ in range(V)]
#
#     # Add edges to the graph
#     add_edge(adj, 0, 1)
#     add_edge(adj, 0, 2)
#     add_edge(adj, 1, 3)
#     add_edge(adj, 1, 4)
#     add_edge(adj, 2, 4)
#
#     # Perform BFS traversal starting from vertex 0
#     print("BFS starting from 0: ")
#     bfs(adj, 0)
#
#     problem = parse_problem("data/problems/probBLOCKS-50-1.pddl.txt")
#     print("Objects:", problem["objects"])
#     print("Initial State:", problem["initial_state"])
#     print("Goal State:", problem["goal_state"])

# from collections import deque
# from blocks_world.problem_parser import parse_problem
#
# # BFS from given source s
# def bfs(adj, s):
#     # Create a queue for BFS
#     q = deque()
#
#     # Initially mark all the vertices as not visited
#     # When we push a vertex into the q, we mark it as
#     # visited
#     visited = [False] * len(adj);
#
#     # Mark the source node as visited and enqueue it
#     visited[s] = True
#     q.append(s)
#
#     # Iterate over the queue
#     while q:
#
#         # Dequeue a vertex from queue and print it
#         curr = q.popleft()
#         print(curr, end=" ")
#
#         # Get all adjacent vertices of the dequeued
#         # vertex. If an adjacent has not been visited,
#         # mark it visited and enqueue it
#         for x in adj[curr]:
#             if not visited[x]:
#                 visited[x] = True
#                 q.append(x)
#
#
# # Function to add an edge to the graph
# def add_edge(adj, u, v):
#     adj[u].append(v)
#     adj[v].append(u)


