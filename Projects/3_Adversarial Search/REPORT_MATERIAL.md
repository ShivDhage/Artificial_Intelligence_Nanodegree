# Adversarial Search Project Report

## Project Overview

This report documents the implementation and evaluation of a knights Isolation agent in `my_custom_player.py`. My chosen approach is the advanced heuristic option, comparing a new evaluation function against sample baseline agents.

## Implementation

### Agent Design
- `CustomPlayer` inherits from `DataPlayer`.
- Uses **minimax search** with **alpha-beta pruning**.
- Uses **iterative deepening** to produce the best available move within the 150ms limit.
- Ensures a legal move is always queued before timeout.

### Custom Heuristic
The heuristic is custom and goes beyond the lecture mobility heuristic.

1. **Liberty advantage**
   - `len(own_liberties) - len(opp_liberties)`
   - This factor captures the relative mobility of the agent compared to the opponent.
   - It is critical because the player with more moves is less likely to become trapped.

2. **Centrality**
   - Prefers moves closer to the center of the board.
   - Central positions allow knights to reach more future squares than edge positions.

3. **Board openness**
   - Uses the number of remaining open cells.
   - Encourages maintaining flexibility and reduces the risk of early self-entrapment.

### Combined Score
The heuristic score is:
- `10.0 * liberty_advantage`
- `+ 1.0 * centrality_score`
- `+ 0.1 * openness_score`

This weighting emphasizes mobility while using centrality and openness to refine state evaluation.

## Experiments and Results

### Baseline Selection
The baseline is the sample Greedy agent, whose behavior is based on immediate board mobility. Fair matches were used to reduce the impact of favorable opening moves.

### Results

| Opponent | Rounds | Games | Fair Matches | Win Rate |
|---|---:|---:|:---:|---:|
| Greedy Agent | 10 | 40 | Yes | 100% |
| Minimax Agent | 5 | 10 | No | 80% |

### Match Setup
- Greedy baseline: `run_match.py -r 10 -o GREEDY -f`
- Minimax comparison: `run_match.py -r 5 -o MINIMAX`

## Analysis

### Advanced Heuristic Questions
**Question 1: What features of the game does your heuristic incorporate, and why do you think those features matter in evaluating states during search?**  
The heuristic incorporates liberty advantage (own liberties minus opponent liberties), centrality (preference for board center positions), and board openness (ratio of remaining open cells). These features matter because liberty advantage directly measures immediate survival potential and winning likelihood, centrality improves long-term mobility by avoiding edge traps where knight moves are constrained, and board openness encourages flexible play that reduces the risk of self-entrapment and preserves strategic options throughout the game.

**Question 2: Analyze the search depth your agent achieves using your custom heuristic. Does search speed matter more or less than accuracy to the performance of your heuristic?**  
Using iterative deepening, the agent typically achieves a search depth of 3 to 4 plies within the 150ms time limit, depending on board complexity and available moves. Search speed is equally important as accuracy in this implementation—while accuracy enables better move selection through stronger heuristic evaluation and alpha-beta pruning, speed ensures the agent always returns a valid move before timeout, balancing tactical depth with practical responsiveness.

## Conclusion
The agent uses a custom heuristic that combines mobility, centrality, and board openness. Experimental results show the approach is effective against the sample Greedy baseline and competitive against the sample Minimax agent.

