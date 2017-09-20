from collections import deque

BOARD_SIZE = 8

def is_valid_position(pos):
    """
    Determines if a board position is valid

    Args:
        pos: tuple of (x,y) position

    Returns:
        bool, whether or not the position is valid given our board size.
    """
    return(pos[0] >= 0 and pos[0] < BOARD_SIZE and
           pos[1] >= 0 and pos[1] < BOARD_SIZE)


def king_gen_moves(pos):
    """
    Creates a generator for the valid moves of a king from the given position.

    Args:
        pos: tuple of (x,y) position

    Returns:
        A generator that generates the set of valid moves of a king from
        the given position.
    """
    for xdelta in [0, 1, -1]:
        for ydelta in [0, 1, -1]:
            tmp = (pos[0] + xdelta, pos[1] + ydelta)

            # are we still on the board after the move
            if is_valid_position(tmp):
                yield(tmp)

def bishop_gen_moves(pos):
    """
    Creates a generator for the valid moves of a bishop from the given position.

    Args:
        pos: tuple of (x,y) position

    Returns:
        A generator that generates the set of valid moves of a bishop from
        the given position.
    """
    for delta in [(1,1), (1,-1), (-1,1), (-1,-1)]:
        for t in range(1, 8):
            tmp = (pos[0] + t*delta[0], pos[1] + t*delta[1])

            # are we still on the board after the move
            if is_valid_position(tmp):
                yield(tmp)

def knight_gen_moves(pos):
    """
    Creates a generator for the valid moves of a knight from the given position.

    Args:
        pos: tuple of (x,y) position

    Returns:
        A generator that generates the set of valid moves of a knight from
        the given position.
    """
    for xdelta in [1, 2, -1, -2]:
        for ydelta in [1, 2, -1, -2]:
            # ensure you are paring a move of distance 2 in one
            # direction with one of distance 1
            if abs(xdelta) + abs(ydelta) == 3:
                tmp = (pos[0] + xdelta, pos[1] + ydelta)

                # are we still on the board after the move
                if is_valid_position(tmp):
                    yield(tmp)

def search(start, goal, gen_moves):
    """
    Find the minimum number of moves needed to get from start to goal position
    given the generator dictated by which chess piece you choose.

    Args:
        start: tuple of (x,y) for the start position
        goal: tuple of (x,y) for the goal position
        gen_moves: a generator that yields the set of valid moves given the
                   current position.

    Returns:
        The minumum number of moves required to get from the start to the
        goal position and -1 if no path exists between the two positions.
    """
    assert is_valid_position(start) and is_valid_position(goal)

    visited = {start: 0}
    frontier = deque([start])

    while len(frontier) > 0:
        node = frontier.popleft()
        if node == goal:
            return(visited[node])

        for move in gen_moves(node):
            if not move in visited:
                visited[move] = visited[node] + 1
                frontier.append(move)
    return(-1)

# deal with the difference reading input in python 2 vs python 3
# if we are using 3 we will get a NameError using raw_input
def my_input(prompt):
    try:
        return(raw_input(prompt))
    except NameError:
        return(input(prompt))

if __name__ == "__main__":
    while True: 
        inputstr = my_input("=> ")

        if inputstr in ["q", "quit", "exit"]:
            break

        try:
            args = inputstr.strip().split(' ')
            start = (int(args[0]), int(args[1]))
            goal = (int(args[2]), int(args[3]))
            piece = args[4]

        except Exception:
            print("'{0}' is not a valid input.".format(inputstr))
            continue

        if piece == "king":
            gen_moves = king_gen_moves
        elif piece == "bishop":
            gen_moves = bishop_gen_moves
        elif piece == "knight":
            gen_moves = knight_gen_moves
        else:
            print("Please enter a valid piece: [king | bishop | knight]")

        try:
            result = search(start, goal, gen_moves)
        except AssertionError:
            print "Either the start or the goal is not a valid board position."
            continue

        if result >= 0:
            print("The {0} takes {1} moves to get from {2} to {3}".format(
                piece, result, start, goal))
        else:
            print("It is not possible for the {0} to get from {1} to {2}.".format(
                piece, start, goal))
