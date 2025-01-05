import re

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
    obj_match = re.search(r'\(:objects (.*?)\)', data, re.DOTALL)
    if not obj_match:
        print("No :INIT section found in the file.")
        return []
    else:
        objects = obj_match.group(1).split()

    # Parse initial state
    init_match = re.search(r'\(:INIT\s*(\(.*?\))*\)', data, re.DOTALL)
    if not init_match:
        print("No :INIT section found in the file.")
    else:
        # Extract from the object returned by the re.search
        raw_init = init_match.group(1)

        # Use regex to extract each item within parentheses
        initial_state = re.findall(r'\((.*?)\)', raw_init)

        # # todo from here on
        # init_lines = raw_init.splitlines()
        # for line in init_lines:
        #     stripped_line = line.strip()
        #     if not stripped_line:
        #         continue
        #
        #     cleaned_line = stripped_line.strip('()')
        #     initial_state.append(cleaned_line)

    # # Parse goal state
    # '\(:goal\s*(\AND(.*?\))*\)' # TO CHANGE
    # goal_match = re.search(r'\(:goal \(AND(.*?)\)\)', data, re.DOTALL)

    # Parse goal state
    goal_match = re.search(r'\(:goal\s*\(AND\s*(.*?)\)\)', data, re.DOTALL)

    if goal_match:
        # # Extract each goal condition and clean it
        # goal_state = [stmt.strip('()') for stmt in goal_match.group(1).split('\n') if stmt.strip()]
        # Extract and clean each goal condition
        goal_state = [stmt.strip('()').strip() for stmt in goal_match.group(1).splitlines() if stmt.strip()]

    # Return parsed data
    return {
        "objects": objects,
        "initial_state": initial_state,
        "goal_state": goal_state
    }


def print_data(input_file, output_file):
    """
    Print the extracted data from a PDDL file and their data types.
    """

    # Parse the data
    parsed_data = parse_problem(input_file)

    for key, value in parsed_data.items():
        # Print the data to the console
        print(f"{key}: {value} (Type: {type(value).__name__})")