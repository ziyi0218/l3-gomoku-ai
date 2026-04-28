# Experiment 1: Alpha-Beta pruning effectiveness

This experiment compares three search variants under identical conditions:

- Minimax
- Alpha-Beta without move ordering
- Alpha-Beta with move ordering

Fixed conditions:

- Board size: 15x15
- Candidate generator: `generate_candidate_moves(board, radius=2)`
- Evaluation function: Eval B / `eval_intermediate`
- Fixed positions: `experiments/experiment1_search/positions.py`
- Default depths: 1, 2, 3

Run:

```bash
python experiments/experiment1_search/benchmark_search.py
```

Optional slower run with repeated timing:

```bash
python experiments/experiment1_search/benchmark_search.py --repeats 3
```

Outputs:

- `experiments/experiment1_search/results/search_benchmark.csv`
- `experiments/experiment1_search/results/search_benchmark_summary.csv`
- `experiments/experiment1_search/results/search_benchmark_summary.md`
- `experiments/experiment1_search/results/fixed_positions.txt`

Export fixed positions as terminal-style boards:

```bash
python experiments/experiment1_search/export_positions.py
```

Optional plots:

```bash
python experiments/experiment1_search/plot_search_benchmark.py
```

This optional plotting script requires `matplotlib`. The CSV and Markdown
outputs are sufficient for the report if plotting dependencies are unavailable.

Plot outputs:

- `experiments/experiment1_search/results/nodes_vs_depth.png`
- `experiments/experiment1_search/results/time_vs_depth.png`
- `experiments/experiment1_search/results/cutoffs_vs_depth.png`

Notes:

- Depth 4 is intentionally not part of the default run because pure Minimax
  becomes slow on the denser fixed positions.
- Alpha-Beta and Minimax should produce the same best score. If best moves differ
  while scores match, that usually means multiple moves are tied under the fixed
  evaluation function.
