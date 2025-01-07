from blocks_world.state import move


def generate_neighbors(state):
    """
    Generate all valid neighbor states from the current state.
    :param state: BlockWorldState object.
    :return: List of BlockWorldState objects representing neighbor states.
    """
    neighbors = []

    # Generate moves for each clear block
    for block in state.clear:
        # Move block to another block
        for destination in state.clear:
            if block != destination:
                new_state = move(state, block, "TABLE" if block in state.onTable else state.on.get(block), destination)
                neighbors.append(new_state)

        # Move block to the table
        if block not in state.onTable:
            new_state = move(state, block, state.on.get(block), "TABLE")
            neighbors.append(new_state)

    return neighbors


def build_graph(initial_state):
    """
    Build the state space graph starting from the initial state.
    :param initial_state: BlockWorldState representing the initial state.
    :return: Dictionary representing the graph (nodes and edges).
    """
    graph = {}  # Dictionary to store the graph
    visited = set()  # Track visited states
    queue = [initial_state]  # BFS queue

    while queue:
        current_state = queue.pop(0)  # Dequeue a state
        if current_state in visited:
            continue

        visited.add(current_state)  # Mark as visited
        neighbors = generate_neighbors(current_state)  # Generate neighbor states
        graph[current_state] = neighbors  # Add to the graph

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)

    return graph


def print_graph(graph):
    """
    Print the graph dictionary in a readable format and display the total number of nodes.
    :param graph: Dictionary where keys are BlockWorldState nodes and values are lists of neighbor nodes.
    """
    print("\nGraph Representation:")
    print("=" * 50)
    for i, (node, neighbors) in enumerate(graph.items(), start=1):
        print(f"Node {i}: {node}")
        print("  Neighbors:")
        for neighbor in neighbors:
            print(f"    - {neighbor}")
        print("-" * 50)

    # Print the total number of nodes
    print(f"\nTotal number of nodes: {len(graph)}")
