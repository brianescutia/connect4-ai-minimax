# connect4-ai-minimax
AI agent for Connect 4 using Minimax and Alpha-Beta Pruning with competitive play against Monte Carlo and Random agents.

# Connect 4 AI – Minimax & Alpha-Beta Pruning

This project implements an AI agent that plays Connect 4 using the Minimax algorithm and Alpha-Beta pruning. Built for the 2024 UC Davis Connect-4 Regional Championship, the agent competes against benchmark AIs under strict performance constraints.

##  Overview

Your AI has 3 seconds per move to decide its best action — the same constraint used in real-time gaming. The project involved designing an evaluation function, implementing classic game tree search algorithms, and benchmarking the AI in tournament-style matches.

## 🤖 Algorithms Implemented

- **minimaxAI:** Basic Minimax search up to a specified depth.
- **alphaBetaAI:** Minimax with Alpha-Beta pruning to reduce the number of explored nodes.
- **monteCarloAI & randomAI:** Benchmark agents provided for testing.

##  Evaluation Function

The evaluation function scores game states based on:
- Number of 2s and 3s in a row
- Blocking opponent threats
- Favoring central positions for control

The AI was tested on:
- 10 matches vs `randomAI`
- 10 matches vs `monteCarloAI`  
With both first and second move scenarios.

##  Running Tests

To evaluate AI performance:
```bash
python3 test.py
