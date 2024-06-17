from collections import deque
import copy

BOARD_LEN = 11

class BoardState:
    def __init__(self, red_coords=None, blue_coords=None, maximising_player=None):
        self.red_coords = red_coords if red_coords is not None else set()
        self.blue_coords = blue_coords if blue_coords is not None else set()
        self.moves = []
        self.maximising_player = maximising_player
    

    def add_coord(self, coord):
        if self.maximising_player == True:
            self.red_coords.add(coord)
        else:
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

    # Returns an array of 4 coordinates of form (row, column)
    def return_moves(self):
        assert len(self.moves) == 4
        return self.moves[0], self.moves[1], self.moves[2], self.moves[3]

    def __str__(self):
        return f"Reds: {sorted(self.red_coords)}, Blues: {sorted(self.blue_coords)}"
    
    def evaluate(self):
        # Here's where we evaluate a state's utility based on a heuristic evaluation function
        # Ideas for this so far: score based on how many tiles each colour has on the board,
        """
        if self.maximising_player:
            heuristic = len(self.find_all_tetrominoes())
        else:
            heuristic = -(len(self.find_all_tetrominoes()))
        """
        heuristic = len(self.red_coords) - len(self.blue_coords)
        return heuristic
    
    # Return True if it is terminal, False if it is not
    def is_terminal_state(self):
        # Here we check if this state is a terminal state, i.e does it have any possible children?
        num_moves = len(self.find_all_tetrominoes())
        if num_moves == 0:
            return True
        return False

    # Finds the 4 surrounding coordinates to a given input coordinate
    # Returns the 4 surrounding coordinates
    def surrounding_coords(self, coord):
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
    def get_playable_coords(self):
        played_coords = self.red_coords | self.blue_coords
        playable_coords = set()

        # If it is reds turn
        if self.maximising_player:
            coords_to_loop = self.red_coords
        # If it is blues turn
        else:
            coords_to_loop = self.blue_coords
        # Find free adjacent coords
        for coord in coords_to_loop:
            for surrounding_coord in self.surrounding_coords(coord):
                # If the surrounding coord is empty then we add it to the set of playable coords
                if surrounding_coord not in played_coords:
                    playable_coords.add(surrounding_coord)
        return playable_coords

    # Finds all tetrominoes avaliable from a given starting node
    def find_tetrominoes(self, start_coord):

        placements = deque()
        placements.append({start_coord})
        played_coords = self.red_coords | self.blue_coords

        # Stores frozen set of valid tetros
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
                surrounding_tiles = self.surrounding_coords(coord)
                possible_moves |= set(surrounding_tiles) - set(current_placement) - played_coords_set

            # Loop through possible moves and add to queue
            for move in possible_moves:
                placements.append(current_placement | {move})
        return combos

    # Finds all playable tetrominoes for a given set of playable coordinates
    # Returns a set of frozenset of actions (must do this as cannot return a set of sets in this case)
    def find_all_tetrominoes(self):
        playable_coords = self.get_playable_coords()

        # Initialize an empty set to store all possible moves
        all_combos = set()

        # Iterate over each starting coordinate
        for playable_coord in playable_coords:
            # Get the tetrominoes for the current starting coordinate
            tetrominoes = self.find_tetrominoes(playable_coord)
            # Merge the results into the set of all possible moves
            all_combos.update(tetrominoes)

        return all_combos

    # create an array of children boards with the tetrominoes added to the board
    def get_board_children(self):
        children_boards = []
        # generate all possible moves from input board state
        possible_tetros = list(self.find_all_tetrominoes())

        # Iterate through generated moves
        for tetro_frozen_set in possible_tetros:
            # Convert frozen set to a list so it becomes iterable
            coords_in_tetro = list(tetro_frozen_set)
            # Add the tetro to the layout of the parent board and return a child board
            child_board = self.play_move(coords_in_tetro)
            # Add the new child board to the array of child boards
            children_boards.append(child_board)
        return children_boards

    def play_move(self, coords_in_tetro):

        # Create a duplicate of parent board
        child_board = copy.deepcopy(self)

        # Reset the array of moves to arrive at new board state
        child_board.moves = []

        # Place each of the new coords into the child object
        for coord in coords_in_tetro:
            child_board.add_coord(coord)
            child_board.moves.append(coord)

        # Remove all full rows and columns as new piece has been played
        child_board.clear_complete_rows_columns()

        # Flip maximising player for the child board
        child_board.maximising_player = not self.maximising_player

        # Print child board for testing purposes

        return child_board

