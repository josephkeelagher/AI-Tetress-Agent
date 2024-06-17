# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord
from collections import deque
import copy
import random

BOARD_LEN = 11

class BoardState:
    def __init__(self, red_coords=None, blue_coords=None):
        self.red_coords = red_coords if red_coords is not None else set()
        self.blue_coords = blue_coords if blue_coords is not None else set()
        self.moves = []

    def add_red(self, coord):

        self.red_coords.add(coord)

    def add_blue(self, coord):

        self.blue_coords.add(coord)

    def clear_complete_rows_columns(self):
                    
        played_coords = self.red_coords | self.blue_coords

        # Function to check if a row is full
        def is_row_full(row):
            return all((row, c) in played_coords for c in range(BOARD_LEN))

        # Function to check if a column is full
        def is_column_full(col):
            return all((r, col) in played_coords for r in range(BOARD_LEN))
        
        full_rows = [row for row in range(BOARD_LEN) if is_row_full(row)]
        full_cols = [col for col in range(BOARD_LEN) if is_column_full(col)]

        # Remove full rows
        for row in full_rows:
            for c in range(BOARD_LEN):
                self.red_coords.discard((row, c))
                self.blue_coords.discard((row, c))
                
        # Remove full columns
        for col in full_cols:
            for r in range(BOARD_LEN):
                self.red_coords.discard((r, col))
                self.blue_coords.discard((r, col))

    def print_board(self):
        for r in range(BOARD_LEN):
            line_str = ""
            for c in range(BOARD_LEN):
                coord = (r, c)
                if coord in self.red_coords:
                    line_str = line_str + "r "
                elif coord in self.blue_coords:
                    line_str = line_str + "b "
                else:
                    line_str = line_str + ". "
            print("                       " + line_str)
        print("")

    def return_moves(self):
        assert len(self.moves) == 4
        return self.moves[0], self.moves[1], self.moves[2], self.moves[3]

    def __str__(self):
        return f"Reds: {sorted(self.red_coords)}, Blues: {sorted(self.blue_coords)}"



class Agent:

    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")
        
        # create an initial board state for the game
        self.initial_state = BoardState()

        # create a "first_move" state to play a predefined move for first game
        self.round_number = 0

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """
        # Below we have hardcoded two actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.
        if self.round_number == 0:
            self.round_number += 1
            match self._color:
                case PlayerColor.RED:
                    return PlaceAction(Coord(5, 3), Coord(6, 3), Coord(7, 3), Coord(8, 3))
                case PlayerColor.BLUE:
                    return PlaceAction(Coord(4, 4), Coord(5, 4), Coord(6, 4), Coord(7, 4))
                
        elif self.round_number < 5:
            self.round_number += 1
            match self._color:
                case PlayerColor.RED:
                    # generate move
                    move = get_board_children_rand(self.initial_state, 'RED')
                    random_move = list(move)
                    c0, c1, c2, c3 = random_move[0], random_move[1], random_move[2], random_move[3]
                    return PlaceAction(Coord(c0[0], c0[1]), Coord(c1[0], c1[1]), Coord(c2[0], c2[1]), Coord(c3[0], c3[1]))
                case PlayerColor.BLUE:
                    move = get_board_children_rand(self.initial_state, 'BLUE')
                    random_move = list(move)
                    c0, c1, c2, c3 = random_move[0], random_move[1], random_move[2], random_move[3]
                    return PlaceAction(Coord(c0[0], c0[1]), Coord(c1[0], c1[1]), Coord(c2[0], c2[1]), Coord(c3[0], c3[1]))
                
        else:
            match self._color:
                case PlayerColor.RED:
                    # generate move
                    move = get_board_children(copy.deepcopy(self.initial_state), 'RED')
                    best_util = float('-inf')
                    curr_util, best_move = minimax(self.initial_state, 2, True, float('-inf'), float('inf'))
                    c0, c1, c2, c3 = best_move
                    """
                    move = get_board_children(copy.deepcopy(self.initial_state), 'RED')
                    best_util = float('-inf')
                    for state in move:
                        curr_util = minimax(state, 2, True, float('-inf'), float('inf'))
                        if curr_util > best_util:
                            best_state = state
                            best_util = curr_util
                    c0, c1, c2, c3 = best_state.return_moves()
                    """
                    

                case PlayerColor.BLUE:
                    move = get_board_children(copy.deepcopy(self.initial_state), 'BLUE')
                    best_util = float('-inf')
                    curr_util, best_move = minimax(self.initial_state, 2, False, float('-inf'), float('inf'))
                    c0, c1, c2, c3 = best_move
                    """
                    move = get_board_children(copy.deepcopy(self.initial_state), 'BLUE')
                    best_util = float('inf')
                    for state in move:
                        curr_util = minimax(state, 2, False, float('-inf'), float('inf'))
                        if curr_util < best_util:
                            best_state = state
                            best_util = curr_util
                    c0, c1, c2, c3 = best_state.return_moves()
                    """
                
        return PlaceAction(Coord(c0[0], c0[1]), Coord(c1[0], c1[1]), Coord(c2[0], c2[1]), Coord(c3[0], c3[1]))

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """
        # If blue played the move
        if color == PlayerColor.BLUE:
            for coord in action.coords:
                self.initial_state.add_blue((coord.r, coord.c))
        # If red played the move
        elif color == PlayerColor.RED:
            for coord in action.coords:
                self.initial_state.add_red((coord.r, coord.c))
        self.initial_state.clear_complete_rows_columns()
        self.initial_state.print_board()
def minimax(state, depth, maximizing_player, alpha, beta):
    """
    This function is called to determine the utility of states up to a certain
    depth which is specified as a parameter 'depth'. 'maximizing_player' is a bool
    which tells the algorithm to either minimise or maximise the utility of a state
    at a certain turn. Alpha-Beta pruning is also used to reduce the branches searched.
    """
    if depth == 0 or is_terminal_state(state, maximizing_player): # is this or bit good?
        return evaluate(state), None
    
    # Trial
    if maximizing_player == True:
        max_util = float('-inf')
        possible_moves = get_board_children(state, "RED")
        ordered_moves = sorted(possible_moves, key=lambda state: evaluate(state), reverse=maximizing_player)
        for child in ordered_moves:
            util, _ = minimax(child, depth - 1, False, alpha, beta)
            if util > max_util:
                max_util = util
                best_move = child.moves()

            if max_util >= beta:
                break
            alpha = max(alpha, max_util)

    else:
        max_util = float('inf')
        possible_moves = get_board_children(state, "BLUE")
        ordered_moves = sorted(possible_moves, key=lambda state: evaluate(state), reverse=maximizing_player)
        for child in ordered_moves:
            util, _ = minimax(child, depth - 1, True, alpha, beta)
            if util < max_util:
                max_util = util
                best_move = child.moves()

            if max_util <= beta:
                break
            alpha = min(alpha, max_util)

    return max_util, best_move

    # When minimizing player find the minimum util
    # Since RED always begins the game, RED will be the maximizing player at the start of the game
    if maximizing_player == True:
        max_util = float('-inf')
        
        for child in get_board_children(state, "RED"):
            util = minimax(child, depth - 1, False, alpha, beta)
            max_util = max(util, max_util)
            alpha = max(alpha, max_util)
            if beta <= alpha:
                break
        return max_util
    else:
        min_util = float('inf')
        for child in get_board_children(state, "BLUE"):
            util = minimax(child, depth - 1, True, alpha, beta)
            min_util = min(util, min_util)
            beta = min(beta, min_util)
            if beta <= alpha:
                break
        return min_util
    
def evaluate(state):
    # Here's where we evaluate a state's utility based on a heuristic evaluation function
    # Ideas for this so far: score based on how many tiles each colour has on the board,

    heuristic = 0
    """
    # positive points for red tiles
    heuristic += len(state.red_coords)
    
    # negative points for blue tiles
    heuristic -= len(state.blue_coords)
    """
    # positive points for RED's possible moves
    heuristic += len(find_all_tetrominoes(state, 'RED'))
    
    # negative points for BLUE's possible moves
    heuristic -= len(find_all_tetrominoes(state, 'BLUE'))

    return heuristic

# Return True if it is terminal, False if it is not
def is_terminal_state(state, maximizing_player):
    # Here we check if this state is a terminal state, i.e does it have any possible children?
    if maximizing_player:
        if (len(find_all_tetrominoes(state, 'RED')) == 0):
            return True
        else:
            return False
    else:
        if (len(find_all_tetrominoes(state, 'BLUE')) == 0):
            return True
        else:
            return False

def get_possible_moves(state):
    # Here is where we return the possible board states that are children of the current node
    return 0

# Finds the 4 surrounding coordinates to a given input coordinate
# Returns the 4 surrounding coordinates
def surrounding_coords(coord):
        coord_r = coord[0]
        coord_c = coord[1]
        above = (coord_r - 1) % BOARD_LEN
        below = (coord_r + 1) % BOARD_LEN
        left = (coord_c - 1) % BOARD_LEN
        right = (coord_c + 1) % BOARD_LEN
        above_coord = (above, coord_c)
        below_coord = (below, coord_c)
        left_coord = (coord_r, left)
        right_coord = (coord_r, right)
        return above_coord, below_coord, left_coord, right_coord

# Finds all playable coordinates given red and blue coordinates as input
# Returns all playable coordinates
# player colour should either be 'RED' or 'BLUE'
def get_playable_coords(board_state, player_colour):
    played_coords = board_state.red_coords | board_state.blue_coords
    playable_coords = set()
    if player_colour == 'RED':
        coords_to_loop = board_state.red_coords
    elif player_colour == 'BLUE':
        coords_to_loop = board_state.blue_coords
    
    for coord in coords_to_loop:
        for surrounding_coord in surrounding_coords(coord):
            if surrounding_coord not in played_coords:
                playable_coords.add(surrounding_coord)
    return playable_coords

# Finds all tetrominoes avaliable from a given starting node
def find_tetrominoes(start_coord, played_coords):
    placements = deque()
    placements.append({start_coord})

    combos = set()

    played_coords_set = set(played_coords)

    # find all possible moves to add to placements
    while placements:

        # Access first placement set in queue
        current_placement = placements.popleft()

        if len(current_placement) == 4:
            combos.add(frozenset(current_placement))  # Convert to frozenset for set of sets
            continue

        possible_moves = set()

        # Loop through each tile in the current placement
        for coord in current_placement:
            surrounding_tiles = surrounding_coords(coord)
            possible_moves |= set(surrounding_tiles) - set(current_placement) - played_coords_set

        # Loop through possible moves and add to queue
        for move in possible_moves:
            placements.append(current_placement | {move})
    return combos

# Finds all playable tetrominoes for a given set of playable coordinates
# Returns a set of frozenset of actions (must do this as cannot return a set of sets in this case)
def find_all_tetrominoes(board_state, player_colour):
    playable_coords = get_playable_coords(board_state, player_colour)
    played_coords = board_state.red_coords | board_state.blue_coords

    all_combos = set()  # Initialize an empty set to store all possible moves

    # Iterate over each starting coordinate
    for playable_coord in playable_coords:
        # Get the tetrominoes for the current starting coordinate
        tetrominoes = find_tetrominoes(playable_coord, played_coords)
        # Merge the results into the set of all possible moves
        all_combos.update(tetrominoes)

    return all_combos

# create an array of children boards with the tetrominoes added to the board
def get_board_children(board_state, player_colour):
    boards = []
    # generate all possible moves from input board state
    moves = find_all_tetrominoes(board_state, player_colour)
    possible_moves = list(moves)
    # Iterate through generated moves
    for frozen_set in possible_moves:

        new_board = copy.deepcopy(board_state)

        new_board.moves = []
        moves_list = list(frozen_set)
        # Add the move tiles to the new child board
        for tile in moves_list:
            new_board.moves.append(tile)
            if player_colour == 'RED':
                new_board.add_red(tile)
            elif player_colour == 'BLUE':
                new_board.add_blue(tile)
        # new_board.print_board()
        # Add child board to list of possible board states generated from input board
        new_board.clear_complete_rows_columns()
        new_board.print_board()
        boards.append(new_board)
    return boards

def order_moves(moves):
    return 0

def get_board_children_rand(board_state, player_colour):
    boards = []
    possible_moves = find_all_tetrominoes(board_state, player_colour)

    # Test I will pick a random move to play
    new_list = list(possible_moves)
    random_index = random.randint(0, (len(new_list) - 1))

    return new_list[random_index]
