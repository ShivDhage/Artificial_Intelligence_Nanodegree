# Adversarial Search Project Report

## Project Overview

This report documents the implementation and evaluation of a knights Isolation agent in `my_custom_player.py`. The chosen approach is the advanced heuristic option, comparing a new evaluation function against sample baseline agents.

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
- Features included: liberty advantage, centrality, and board openness.
- These features matter because:
  - liberty advantage directly relates to survival and winning potential;
  - centrality improves future mobility for knight moves;
  - board openness preserves options and reduces the risk of losing by confinement.

### Search Depth and Tradeoffs
- Iterative deepening lets the agent search to successively higher depths until the 150ms limit.
- In practice, the agent generally reaches a depth of around 3 to 4 plies depending on board complexity.
- Search speed is important because the agent must return a move on time, but accuracy is also important because a stronger heuristic enables better pruning and move ordering.
- Alpha-beta pruning balances both: it allows deeper search while preserving the quality of the chosen move.

## Validation

All required tests in `tests/test_my_custom_player.py` passed:
- `test_get_action_player1`
- `test_get_action_player2`
- `test_get_action_midgame`
- `test_get_action_terminal`
- `test_custom_player`

## Conclusion
The agent uses a custom heuristic that combines mobility, centrality, and board openness. Experimental results show the approach is effective against the sample Greedy baseline and competitive against the sample Minimax agent.

