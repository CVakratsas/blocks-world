class BlockWorldState:
    """
    Represents a state in the Blocks World problem.
    """

    def __init__(self, clear=None, onTable=None, on=None, handEmpty=True, action=None):
        """
        Initialize the state.
        :param clear: Set of blocks that are clear (nothing on top).
        :param onTable: Set of blocks that are on the table.
        :param on: Dictionary mapping blocks to what they are on.
        :param handEmpty: Boolean indicating whether the hand is empty.
        :param action: The action that led to this state (e.g., 'Move A to B').
        """
        self.clear = clear or set()
        self.onTable = onTable or set()
        self.on = on or {}  # Maps a block to what it's on
        self.handEmpty = handEmpty
        self.action = action

    def __repr__(self):
        return (
            f"BlockWorldState(clear={self.clear}, "
            f"onTable={self.onTable}, on={self.on}, handEmpty={self.handEmpty})"
        )

    def __eq__(self, other):
        if not isinstance(other, BlockWorldState):
            return False
        # Only compare the 'on' mapping to determine goal equivalence
        return self.on == other.on

    def __hash__(self):
        return hash((frozenset(self.clear), frozenset(self.onTable), frozenset(self.on.items()), self.handEmpty))

    def to_dict(self):
        """
        Convert the state to a dictionary representation.
        """
        return {
            "clear": self.clear,
            "onTable": self.onTable,
            "on": self.on,
            "handEmpty": self.handEmpty,
        }

    def copy(self):
        """
        Create a deep copy of the BlockWorldState object.
        :return: A new BlockWorldState object with the same attributes.
        """
        return BlockWorldState(
            clear=self.clear.copy(),
            onTable=self.onTable.copy(),
            on=self.on.copy(),
            handEmpty=self.handEmpty,
            action=self.action
        )

    @classmethod
    def from_data(cls, clear, onTable, on, handEmpty=True):
        """
        Create a BlockWorldState from data components.
        """
        return cls(clear=set(clear), onTable=set(onTable), on=dict(on), handEmpty=handEmpty)


def move(state, block, from_location, to_location):
    """
    Apply a move action to a state.
    :param state: BlockWorldState object.
    :param block: Block to move.
    :param from_location: Location to move the block from ('TABLE' or another block).
    :param to_location: Location to move the block to ('TABLE' or another block).
    :return: Modified BlockWorldState object.
    """

    new_state = state.copy()  # Create a copy of the current state

    # Remove the block from its current location
    if from_location == "TABLE":
        new_state.onTable.remove(block)
    else:
        new_state.on.pop(block)

    # Update the 'CLEAR' set for the source location
    if from_location != "TABLE":
        new_state.clear.add(from_location)

    # Place the block in the new location
    if to_location == "TABLE":
        new_state.onTable.add(block)
    else:
        new_state.on[block] = to_location
        new_state.clear.remove(to_location)

    # Update 'CLEAR' for the moved block
    new_state.clear.add(block)

    # Add action description
    new_state.action = f"Move {block} from {from_location} to {to_location}"

    return new_state

