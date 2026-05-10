# Experiment 4: Final Difficulty Tournament

Experiment 4 validates Easy / Medium / Hard AI difficulty settings using fixed
opening positions and round-robin tournaments.

This folder currently keeps two result sets:

|Result folder|Setup|Purpose|
|---|---|---|
|`result(A1_A3_B2)`|Easy = A1, Medium = A3, Hard = B2|Earlier final setup.|
|`result(A1_B2_B3)`|Easy = A1, Medium = B2, Hard = B3|Updated recommended setup after the Eval B rerun.|

## Recommended Final Configurations

|Difficulty|Profile|Search|Evaluation|Depth|Candidate radius|
|---|---|---|---|---|---|
|Easy|A1|Alpha-Beta|Eval A|1|2|
|Medium|B2|Alpha-Beta + ordering|Eval B|2|3|
|Hard|B3|Alpha-Beta + ordering|Eval B|3|2|

## Tournament Protocol

- 3 difficulty AIs: Easy, Medium, Hard.
- Round-robin tournament.
- 3 pairs total.
- Fixed opening positions.
- Max moves: 50.
- Draws occur when the game reaches the max-move limit.

The current result folders have different sample sizes:

- `result(A1_A3_B2)`: 200 games per pair, 600 games total.
- `result(A1_B2_B3)`: 50 games per pair, 150 games total.

## Outputs

Each result folder contains:

- `difficulty_match_results.csv`
- `difficulty_ai_ranking.csv`
- `difficulty_ai_ranking.md`
- `difficulty_pairwise_summary.csv`
- `difficulty_cumulative_blue_win_rate.png`
- `difficulty_strength_vs_time.png`
- `difficulty_pairwise_score_heatmap.png`
- `difficulty_color_win_rate.png`

## How to Reproduce

Run the tournament:

```bash
python experiments/experiment4_difficulty_tournament/tournament.py
```

Regenerate plots:

```bash
python experiments/experiment4_difficulty_tournament/plot_difficulty_tournament.py
```

See `REPORT.md` for the comparison between both result sets.
