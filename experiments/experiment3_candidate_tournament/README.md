# Experiment 3: Candidate AI Selection Tournament

This experiment screens candidate AI configurations before the final
Easy / Medium / Hard tournament.

The current experiment uses six deterministic Alpha-Beta candidates:

|AI|Search|Evaluation|Depth|
|---|---|---|---|
|A1|Alpha-Beta + ordering|Eval A|1|
|B1|Alpha-Beta + ordering|Eval B|1|
|A2|Alpha-Beta + ordering|Eval A|2|
|B2|Alpha-Beta + ordering|Eval B|2|
|A3|Alpha-Beta + ordering|Eval A|3|
|B3|Alpha-Beta + ordering|Eval B|3|

Excluded profiles:

- C1 is excluded because Eval C at depth 1 is too shallow to show the value of
  five-window potential.
- C3 is excluded because Experiment 2 showed Eval C at depth 3 is too slow.
- Depth 4 is not tested.

Run the default candidate tournament:

```bash
python experiments/experiment3_candidate_tournament/candidate_tournament.py
```

Default protocol:

- 6 candidate AIs
- 15 pairings
- 10 games per pair
- 5 games with each AI as black
- `max_moves = 50`
- output directory: `experiments/experiment3_candidate_tournament/results`

Parallel execution is enabled by default with `--workers 4`. Because all AIs are
deterministic, the script computes each unique black/white pairing once and then
expands the repeated games into the full 150-row result table. This preserves the
same tournament protocol while avoiding repeated identical searches.

For a single-worker run:

```bash
python experiments/experiment3_candidate_tournament/candidate_tournament.py --workers 1
```

For a faster smoke run:

```bash
python experiments/experiment3_candidate_tournament/candidate_tournament.py --games-per-pair 2 --max-moves 40
```

Outputs:

- `results/candidate_match_results.csv`
- `results/candidate_ai_ranking.csv`
- `results/candidate_ai_ranking.md`
- `results/candidate_pairwise_summary.csv`

Generate plots from the existing CSV results:

```bash
python experiments/experiment3_candidate_tournament/plot_candidate_tournament.py
```

Plot outputs:

- `results/candidate_win_rate.png`
- `results/candidate_avg_time.png`
- `results/candidate_strength_vs_time.png`

Current final results are stored in `results`. The old `results2` staging
directory has been removed.
