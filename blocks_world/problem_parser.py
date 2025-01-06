import re

from blocks_world.state import BlockWorldState


def parse_problem(file_path):
    """
    Parse a PDDL problem file and return the initial state, goal state, and objects.
    """
    # Define structures to hold the parsed data
    objects = []
    initial_state = []
    goal_state = []

    # Open and read the file
    with open(file_path, 'r') as file:
        data = file.read()

    # Parse objects
    obj_match = re.search(r'\(:objects (.*?)\)', data, re.DOTALL | re.IGNORECASE)
    if not obj_match:
        print("No :INIT section found in the file.")
        return []
    else:
        objects = obj_match.group(1).split()

    # Parse initial state
    init_match = re.search(r'\(:init\s*(\(.*?\))*\)', data, re.DOTALL | re.IGNORECASE)
    if not init_match:
        print("No :INIT section found in the file.")
    else:
        # Extract from the object returned by the re.search
        raw_init = init_match.group(1)

        # Use regex to extract each item within parentheses
        initial_state = re.findall(r'\((.*?)\)', raw_init)

    # Parse goal state
    goal_match = re.search(r'\(:goal\s*\(AND(.*)\)\)', data, re.DOTALL | re.IGNORECASE)
    if not goal_match:
        print("No :goal section found in the file.")
    else:
        # Captures the raw content inside the AND block
        raw_goal = goal_match.group(1).strip()

        # Extract individual conditions from raw data
        goal_state = re.findall(r'\((.*?)\)', raw_goal)

    # Return parsed data
    return {
        "objects": objects,
        "initial_state": initial_state,
        "goal_state": goal_state
    }

def extract_state(initial_state_list):
    """
    Transform the initial state list into a BlockWorldState object.
    """
    clear = set()
    onTable = set()
    on = {}

    for state in initial_state_list:
        parts = state.split()
        if parts[0] == "CLEAR":
            clear.add(parts[1])
        elif parts[0] == "ONTABLE":
            onTable.add(parts[1])
        elif parts[0] == "ON":
            on[parts[1]] = parts[2]

    # Handempty is always assumed True unless explicitly stated otherwise
    handEmpty = True

    return BlockWorldState(clear=clear, onTable=onTable, on=on, handEmpty=handEmpty)


def print_data(input_file, output_file):
    """
    Print the extracted data from a PDDL file and their data types.
    """

    # Parse the data
    parsed_data = parse_problem(input_file)

    for key, value in parsed_data.items():
        # Print the data to the console
        print(f"{key}: {value} (Type: {type(value).__name__})")