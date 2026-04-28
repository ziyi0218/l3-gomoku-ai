# Experiment 2: Evaluation function comparison

This experiment compares three evaluation functions under the same search setup:

- Eval A: consecutive segment length
- Eval B: segment length plus open/blocked ends
- Eval C: five-cell window potential plus center bonus

Fixed conditions:

- Search: Alpha-Beta + move ordering
- Board size: 15x15
- Candidate generator: `generate_candidate_moves(board, radius=2)`
- Depths: 1, 2, 3
- Fixed positions: `experiments/experiment2_evaluations/positions.py`

Run:

```bash
python experiments/experiment2_evaluations/compare_evaluations.py
```

Outputs:

- `experiments/experiment2_evaluations/results/evaluation_comparison.csv`
- `experiments/experiment2_evaluations/results/evaluation_comparison_summary.csv`
- `experiments/experiment2_evaluations/results/evaluation_comparison_summary.md`
- `experiments/experiment2_evaluations/results/evaluation_best_move_diff.csv`

Export fixed positions as terminal-style boards:

```bash
python experiments/experiment2_evaluations/export_positions.py
```

Generate plots:

```bash
python experiments/experiment2_evaluations/plot_evaluation_comparison.py
```

Plot outputs:

- `eval_time_vs_depth.png`
- `eval_nodes_vs_depth.png`
- `eval_cutoffs_vs_depth.png`
- log-scale versions for time and nodes

Install plotting dependency if needed:

```bash
python -m pip install -r requirements.txt
```
