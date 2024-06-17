from referee.game import PlayerColor, Action, PlaceAction, Coord
from . import BoardState
from . import MiniMax

class Agent:

    """
    This class is the "entry point" for the agent, providing an interface to
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
            move1 = ((1,1), (1,2), (1,3), (1,4))
            move_1_valid = True
            for tile in move1:
                if tile in self.initial_state.red_coords | self.initial_state.blue_coords:
                    move_1_valid = False
                    break
            self.round_number += 1
            if move_1_valid:
                return PlaceAction(Coord(1, 1), Coord(1, 2), Coord(1, 3), Coord(1, 4))
            else:
                # If the initial move is not playable then we fall back to this move
                return PlaceAction(Coord(7, 5), Coord(7, 6), Coord(7, 7), Coord(7, 8))
                
        else:
            # Find the optimal move as determined by minimax
            match self.initial_state.maximising_player:
                case True:
                    _, best_move = MiniMax.minimax(self.initial_state, 3, self.initial_state.maximising_player, float('-inf'), float('inf'))
                    c0, c1, c2, c3 = best_move
                    

                case False:
                    _, best_move = MiniMax.minimax(self.initial_state, 3, self.initial_state.maximising_player, float('-inf'), float('inf'))
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