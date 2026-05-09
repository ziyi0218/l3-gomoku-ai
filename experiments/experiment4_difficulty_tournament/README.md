# Experiment 4: Final Difficulty Tournament

Experiment 4 validates the final Easy / Medium / Hard AI difficulty settings
using a larger deterministic tournament.

The final result set is stored in:

```text
result12/
```

Older intermediate result folders were removed during cleanup.

## Final Configurations

|Difficulty|Profile|Search|Evaluation|Depth|Candidate radius|
|---|---|---|---|---|---|
|Easy|A1|Alpha-Beta|Eval A|1|2|
|Medium|A3|Alpha-Beta + ordering|Eval A|3|2|
|Hard|B2|Alpha-Beta + ordering|Eval B|2|3|

## Tournament Protocol

- 3 difficulty AIs: Easy, Medium, Hard.
- Round-robin tournament.
- 3 pairs total.
- 200 games per pair.
- 600 games total.
- Fixed opening positions are used to avoid evaluating only one deterministic
  game path.
- Max moves: 50.
- Draws occur when the game reaches the max-move limit.

## Outputs

Final CSV and plot outputs are in `result12/`:

- `difficulty_match_results.csv`
- `difficulty_ai_ranking.csv`
- `difficulty_ai_ranking.md`
- `difficulty_pairwise_summary.csv`
- `difficulty_cumulative_blue_win_rate.png`
- `difficulty_strength_vs_time.png`
- `difficulty_pairwise_score_heatmap.png`
- `difficulty_color_win_rate.png`

## How to Reproduce

Run the full tournament:

```bash
python experiments/experiment4_difficulty_tournament/tournament.py
```

Regenerate plots from `result12`:

```bash
python experiments/experiment4_difficulty_tournament/plot_difficulty_tournament.py
```

The default output directory is:

```text
experiments/experiment4_difficulty_tournament/result12
```
