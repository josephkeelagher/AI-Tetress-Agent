def minimax(state, depth, maximizing_player, alpha, beta):
    """
    This function is called to determine the utility of states up to a certain
    depth which is specified as a parameter 'depth'. 'maximizing_player' is a bool
    which tells the algorithm to either minimise or maximise the utility of a state
    at a certain turn. Alpha-Beta pruning is also used to reduce the branches searched.
    """

    if depth == 0 or state.is_terminal_state():
        return state.evaluate(), None
    
    if maximizing_player == True:
        best_util = float('-inf')
        possible_moves = state.get_board_children()
        ordered_moves = sorted(possible_moves, key=lambda move: move.evaluate(), reverse=maximizing_player)[:3]
        for child in ordered_moves:
            util, _ = minimax(child, depth - 1, False, alpha, beta)
            if util > best_util:
                best_util = util
                best_move = child.moves
            
            alpha = max(alpha, best_util)
            if beta <= alpha:
                break
        
            

    else:
        best_util = float('inf')
        possible_moves = state.get_board_children()
        ordered_moves = sorted(possible_moves, key=lambda move: move.evaluate(), reverse=maximizing_player)[:3]
        for child in ordered_moves:
            util, _ = minimax(child, depth - 1, True, alpha, beta)
            if util < best_util:
                best_util = util
                best_move = child.moves

            beta = min(beta, best_util)
            if beta <= alpha:
                break
            

    return best_util, best_move