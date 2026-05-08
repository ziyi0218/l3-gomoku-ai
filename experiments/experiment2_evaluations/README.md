# Experiment 2: Evaluation Function Comparison

This folder contains the fresh Experiment 2 rerun after Eval A was modified.
Old Experiment 2 outputs were discarded before regenerating this folder.

## Run

```bash
python experiments/experiment2_evaluations/compare_evaluations.py
python experiments/experiment2_evaluations/export_positions.py
python experiments/experiment2_evaluations/plot_evaluation_comparison.py
```

## Outputs

- `results/evaluation_comparison.csv`: raw search results.
- `results/evaluation_summary.csv`: averages by depth and evaluation.
- `results/evaluation_best_move_diff.csv`: best-move differences.
- `results/evaluation_positions.txt`: readable fixed boards.
- `results/eval_time_vs_depth.png`: average runtime plot.
- `results/eval_nodes_vs_depth.png`: average node plot.
- `results/eval_cutoffs_vs_depth.png`: average cutoff plot.

## Controlled Conditions

- Board size: 15x15.
- Search: Alpha-Beta + move ordering.
- Candidate generator: `generate_candidate_moves(radius=2)`.
- Depths: 1, 2, 3 only.
- Evaluations: current `eval_basic`, `eval_intermediate`, and `eval_advanced`.
