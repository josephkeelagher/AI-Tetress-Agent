# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord
from . import BoardState
from . import MiniMax

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
        self.initial_state = BoardState.BoardState(maximising_player=True)

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
            match self.initial_state.maximising_player:
                case True:
                    return PlaceAction(Coord(5, 3), Coord(6, 3), Coord(7, 3), Coord(8, 3))
                case False:
                    return PlaceAction(Coord(4, 4), Coord(5, 4), Coord(6, 4), Coord(7, 4))
                
        else:
            match self.initial_state.maximising_player:
                case True:
                    possible_moves = self.initial_state.get_board_children()
                    best_move = sorted(possible_moves, key=lambda move: move.evaluate(), reverse=True)[0].moves
                    c0, c1, c2, c3 = best_move
                    

                case False:
                    possible_moves = self.initial_state.get_board_children()
                    best_move = sorted(possible_moves, key=lambda move: move.evaluate(), reverse=False)[0].moves
                    c0, c1, c2, c3 = best_move
                
        return PlaceAction(Coord(c0[0], c0[1]), Coord(c1[0], c1[1]), Coord(c2[0], c2[1]), Coord(c3[0], c3[1]))

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """
        moves = []
        for coord in action.coords:
            moves.append((coord.r, coord.c))
        self.initial_state = self.initial_state.play_move(moves)