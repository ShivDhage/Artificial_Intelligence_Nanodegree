
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # Use iterative deepening to find the best move within time limit
        # The search automatically stops when time runs out via the timeout mechanism
        best_move = None
        
        # For early game, use a random move
        if state.ply_count < 2:
            import random
            best_move = random.choice(state.actions())
        else:
            # Iterative deepening: try increasing depths
            for depth in range(1, 100):  # Will be cut off by timeout
                move = self.minimax_search(state, depth)
                if move is not None:
                    best_move = move
                    self.queue.put(best_move)
                else:
                    break
            
            # If we found a move, it should already be queued
            # But ensure at least one move is queued
            if best_move is None:
                import random
                best_move = random.choice(state.actions())
        
        # Always queue a move as the fallback
        if best_move is not None:
            self.queue.put(best_move)

    def minimax_search(self, state, depth):
        """ Minimax search with alpha-beta pruning """
        def max_value(state, depth, alpha, beta):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1, alpha, beta))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        def min_value(state, depth, alpha, beta):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1, alpha, beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        # Find the best move by evaluating each action
        best_move = None
        best_value = float("-inf")
        
        for action in state.actions():
            value = min_value(state.result(action), depth - 1, float("-inf"), float("inf"))
            if value > best_value:
                best_value = value
                best_move = action
        
        return best_move

    def score(self, state):
        """ Custom heuristic that combines multiple factors for game evaluation
        
        This heuristic considers:
        1. Liberty advantage (own liberties - opponent liberties) - weighted heavily
        2. Centrality: prefer positions closer to center of board
        3. Board safety: ratio of open cells (encourages leaving options open)
        """
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        
        # Handle None locations (shouldn't happen in normal play after first move)
        if own_loc is None or opp_loc is None:
            return 0
        
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        
        # Primary factor: liberty advantage (this is the most important)
        liberty_score = len(own_liberties) - len(opp_liberties)
        
        # Secondary factor: centrality
        # Board is 11x13 (width x height in the bit representation)
        # Center is around position 60 (middle of the board)
        centrality_score = self._centrality_heuristic(own_loc, opp_loc)
        
        # Tertiary factor: board openness (prefer games with more open cells)
        openness_score = self._board_openness_heuristic(state)
        
        # Combine the factors with weights
        # Liberty advantage is most important (weight 10)
        # Centrality helps in mid-game decisions (weight 1)
        # Board openness is a tiebreaker (weight 0.1)
        combined_score = (
            10.0 * liberty_score +
            1.0 * centrality_score +
            0.1 * openness_score
        )
        
        return combined_score
    
    def _centrality_heuristic(self, own_loc, opp_loc):
        """ Calculate centrality bonus: prefer center positions
        
        The board is 11 columns wide and 9 rows tall
        Center cell is around index 60 in the bitboard representation
        """
        # Board dimensions: 11 width, 13 height (including padding)
        WIDTH = 11
        HEIGHT = 9
        
        # Convert linear index to (row, col)
        def index_to_coord(idx):
            # Account for padding in the bitboard
            row = idx // (WIDTH + 2)
            col = idx % (WIDTH + 2) - 1  # -1 to account for left padding
            return row, col
        
        own_row, own_col = index_to_coord(own_loc)
        opp_row, opp_col = index_to_coord(opp_loc)
        
        # Calculate distance from center
        center_row = HEIGHT / 2.0
        center_col = WIDTH / 2.0
        
        own_dist = ((own_row - center_row) ** 2 + (own_col - center_col) ** 2) ** 0.5
        opp_dist = ((opp_row - center_row) ** 2 + (opp_col - center_col) ** 2) ** 0.5
        
        # Closer to center = higher score
        centrality_bonus = (opp_dist - own_dist)
        
        return centrality_bonus
    
    def _board_openness_heuristic(self, state):
        """ Calculate how open the board is (number of available cells)
        
        This encourages the agent to keep options open by not boxing itself in
        """
        # Count number of open cells on the board
        # In Isolation, open cells are represented by 1 bits in the board
        board = state.board
        open_cells = bin(board).count('1')
        
        # Normalize by total board size (11 x 9 = 99 cells)
        total_cells = 99
        openness = open_cells / total_cells
        
        # Return a score that benefits from more open cells
        # Max score is when board is completely open (openness = 1)
        return openness
