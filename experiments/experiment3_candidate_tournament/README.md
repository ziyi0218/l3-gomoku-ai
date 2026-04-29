# Experiment 3: Candidate AI Selection Tournament

This experiment runs a small round-robin tournament to screen candidate AI
configurations for the final Easy / Medium / Hard setup.

It is not the final formal tournament.

Candidate AIs:

- A1 = Alpha-Beta + ordering + Eval A + depth 1
- B1 = Alpha-Beta + ordering + Eval B + depth 1
- A2 = Alpha-Beta + ordering + Eval A + depth 2
- B2 = Alpha-Beta + ordering + Eval B + depth 2
- C2 = Alpha-Beta + ordering + Eval C + depth 2
- A3 = Alpha-Beta + ordering + Eval A + depth 3
- B3 = Alpha-Beta + ordering + Eval B + depth 3

Excluded:

- C1 is excluded because Eval C at depth 1 is too shallow to show the value of
  five-window potential.
- C3 is excluded because Experiment 2 showed Eval C at depth 3 is too slow.
- Depth 4 is not tested.

Run the default candidate tournament:

```bash
python experiments/experiment3_candidate_tournament/candidate_tournament.py
```

Default protocol:

- 7 candidate AIs
- 21 pairings
- 10 games per pair
- 5 games with each AI as black
- `max_moves = 80`

For a faster smoke run:

```bash
python experiments/experiment3_candidate_tournament/candidate_tournament.py --games-per-pair 2 --max-moves 40
```

If the top candidates remain too close after 10 games per pair:

```bash
python experiments/experiment3_candidate_tournament/candidate_tournament.py --games-per-pair 20
```

Parallel execution is supported:

```bash
python experiments/experiment3_candidate_tournament/candidate_tournament.py --workers 4
```

Outputs:

- `results/candidate_match_results.csv`
- `results/candidate_ai_ranking.csv`
- `results/candidate_ai_ranking.md`
- `results/candidate_pairwise_summary.csv`

Generate plots after running:

```bash
python experiments/experiment3_candidate_tournament/plot_candidate_tournament.py
```

For a custom output directory:

```bash
python experiments/experiment3_candidate_tournament/plot_candidate_tournament.py --results-dir experiments/experiment3_candidate_tournament/results_smoke
```

Plot outputs:

- `candidate_win_rate.png`
- `candidate_avg_time.png`
- `candidate_strength_vs_time.png`
