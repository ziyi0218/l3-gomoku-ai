# Experiment 4 Report: Final Difficulty Tournament

## 1. Objective

Experiment 4 evaluates the final Easy / Medium / Hard difficulty settings for
the Gomoku AI. Unlike Experiment 3, which screened several candidate
configurations, Experiment 4 focuses on the final difficulty ladder.

The current folder contains two result sets:

|Result folder|Difficulty setup|Purpose|
|---|---|---|
|`result(A1_A3_B2)`|Easy = A1, Medium = A3, Hard = B2|Original final setup from the earlier candidate selection.|
|`result(A1_B2_B3)`|Easy = A1, Medium = B2, Hard = B3|Updated setup after the Eval B rerun showed B2/B3 as stronger practical candidates.|

The goal is to check whether the difficulty ladder behaves as expected:

- Hard should be strongest overall.
- Medium should be clearly stronger than Easy.
- Easy should remain fast and weaker.
- Runtime should remain acceptable for each difficulty level.

## 2. AI Configurations

### Setup 1: A1 / A3 / B2

|Difficulty|Profile|Search|Evaluation|Depth|Candidate radius|
|---|---|---|---|---|---|
|Easy|A1|Alpha-Beta|Eval A|1|2|
|Medium|A3|Alpha-Beta + ordering|Eval A|3|2|
|Hard|B2|Alpha-Beta + ordering|Eval B|2|3|

### Setup 2: A1 / B2 / B3

|Difficulty|Profile|Search|Evaluation|Depth|Candidate radius|
|---|---|---|---|---|---|
|Easy|A1|Alpha-Beta|Eval A|1|2|
|Medium|B2|Alpha-Beta + ordering|Eval B|2|3|
|Hard|B3|Alpha-Beta + ordering|Eval B|3|2|

The second setup is motivated by the updated Experiment 3 results, where B3 had
the highest score rate and B2 had a strong strength-runtime trade-off.

## 3. Tournament Protocol

Both result sets use:

- 3 difficulty AIs;
- 3 pairings: Easy vs Medium, Easy vs Hard, Medium vs Hard;
- fixed opening positions;
- max moves: 50;
- draw if max moves is reached.

The difference is the number of games:

|Result folder|Games per pair|Total games|
|---|---:|---:|
|`result(A1_A3_B2)`|200|600|
|`result(A1_B2_B3)`|50|150|

The tournament uses fixed openings rather than a single empty-board start. This
reduces overfitting to one deterministic game path and gives each pair a broader
set of starting positions.

## 4. Overall Results

|Result folder|Games|Black wins|White wins|Draws|Max-move draws|Avg moves|
|---|---:|---:|---:|---:|---:|---:|
|`result(A1_A3_B2)`|600|320|270|10|10|17.57|
|`result(A1_B2_B3)`|150|95|52|3|3|15.26|

Both tournaments have a low draw count. Black has an advantage in both result
sets, especially in `result(A1_B2_B3)`, but white still wins enough games that
the results are not only first-player outcomes.

## 5. Setup 1 Results: A1 / A3 / B2

### Ranking

|AI|Profile|Evaluation|Depth|Games|Wins|Losses|Draws|Win rate|Score rate|Avg time / move ms|Avg nodes / move|Black win rate|White win rate|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Hard|B2|Eval B|2|400|280|110|10|0.7|0.7125|3175.6271|431.85|0.75|0.65|
|Medium|A3|Eval A|3|400|250|140|10|0.625|0.6375|6228.0128|5356.2|0.65|0.6|
|Easy|A1|Eval A|1|400|60|340|0|0.15|0.15|17.6245|76.49|0.2|0.1|

### Pairwise Results

|Pair|Games|AI 1 wins|AI 2 wins|Draws|AI 1 score rate|AI 2 score rate|Interpretation|
|---|---:|---:|---:|---:|---:|---:|---|
|Easy vs Hard|200|40|160|0|0.2|0.8|Hard clearly beats Easy.|
|Easy vs Medium|200|20|180|0|0.1|0.9|Medium clearly beats Easy.|
|Medium vs Hard|200|70|120|10|0.375|0.625|Hard beats Medium, but the gap is moderate.|

This setup validates the ordering:

```text
Hard > Medium > Easy
```

However, Medium is slower than Hard. Medium uses A3, which searches deeper with
Eval A, while Hard uses B2, a shallower but more effective Eval B configuration.

### Plots

![A1/A3/B2 cumulative score](<result(A1_A3_B2)/difficulty_cumulative_blue_win_rate.png>)

![A1/A3/B2 strength-runtime](<result(A1_A3_B2)/difficulty_strength_vs_time.png>)

![A1/A3/B2 pairwise heatmap](<result(A1_A3_B2)/difficulty_pairwise_score_heatmap.png>)

![A1/A3/B2 color win rate](<result(A1_A3_B2)/difficulty_color_win_rate.png>)

## 6. Setup 2 Results: A1 / B2 / B3

### Ranking

|AI|Profile|Evaluation|Depth|Games|Wins|Losses|Draws|Win rate|Score rate|Avg time / move ms|Avg nodes / move|Black win rate|White win rate|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Hard|B3|Eval B|3|100|65|32|3|0.65|0.665|4843.7375|5126.72|0.8|0.5|
|Medium|B2|Eval B|2|100|61|36|3|0.61|0.625|3735.4328|427.67|0.76|0.46|
|Easy|A1|Eval A|1|100|21|79|0|0.21|0.21|21.2439|73.85|0.34|0.08|

### Pairwise Results

|Pair|Games|AI 1 wins|AI 2 wins|Draws|AI 1 score rate|AI 2 score rate|Interpretation|
|---|---:|---:|---:|---:|---:|---:|---|
|Easy vs Hard|50|12|38|0|0.24|0.76|Hard clearly beats Easy.|
|Easy vs Medium|50|9|41|0|0.18|0.82|Medium clearly beats Easy.|
|Medium vs Hard|50|20|27|3|0.43|0.57|Hard beats Medium, but the gap is smaller than in Easy matchups.|

This setup also validates the ordering:

```text
Hard > Medium > Easy
```

Compared with Setup 1, Setup 2 has a more natural difficulty progression:

- Easy is still weak and fast.
- Medium is stronger than Easy and uses the efficient B2 configuration.
- Hard is the strongest and uses deeper Eval B search.

The Medium-Hard gap is smaller in Setup 2, which is expected because both levels
use Eval B. This makes the final ladder smoother, although it also means Medium
and Hard are closer in strength.

### Plots

![A1/B2/B3 cumulative score](<result(A1_B2_B3)/difficulty_cumulative_blue_win_rate.png>)

![A1/B2/B3 strength-runtime](<result(A1_B2_B3)/difficulty_strength_vs_time.png>)

![A1/B2/B3 pairwise heatmap](<result(A1_B2_B3)/difficulty_pairwise_score_heatmap.png>)

![A1/B2/B3 color win rate](<result(A1_B2_B3)/difficulty_color_win_rate.png>)

## 7. Comparison Between the Two Setups

|Criterion|A1 / A3 / B2|A1 / B2 / B3|
|---|---|---|
|Ordering valid?|Yes: Hard > Medium > Easy|Yes: Hard > Medium > Easy|
|Easy behavior|Weak and fast|Weak and fast|
|Medium behavior|Strong, but slower than Hard|Strong and more efficient|
|Hard behavior|Strongest and faster than Medium|Strongest, but slower than Medium|
|Medium-Hard gap|Hard clearly ahead|Hard ahead, but closer|
|Runtime logic|Less intuitive because Medium is slowest|More intuitive because deeper B3 is Hard|

Setup 1 is statistically stronger because it uses 600 games, while Setup 2 uses
150 games. However, Setup 2 matches the updated Experiment 3 conclusions better:
B2 is a strong medium-level candidate and B3 is the strongest candidate among
the practical Eval B configurations.

## 8. First-Player Analysis

Setup 1 color win rates:

```text
Easy black win rate:   0.20
Easy white win rate:   0.10
Medium black win rate: 0.65
Medium white win rate: 0.60
Hard black win rate:   0.75
Hard white win rate:   0.65
```

Setup 2 color win rates:

```text
Easy black win rate:   0.34
Easy white win rate:   0.08
Medium black win rate: 0.76
Medium white win rate: 0.46
Hard black win rate:   0.80
Hard white win rate:   0.50
```

Black has an advantage in both setups. The advantage is more visible in Setup 2,
partly because it has fewer games. This should be mentioned as a limitation when
interpreting the 150-game result set.

## 9. Interpretation

Both result sets support a valid Easy / Medium / Hard ladder. Easy is clearly
weaker than the other two levels, which is desirable for a beginner-level AI.

The main difference is the Medium configuration:

- In Setup 1, Medium = A3. It is stronger than Easy but slower than Hard.
- In Setup 2, Medium = B2. It is stronger than Easy, more efficient than A3, and
  aligns with the updated Experiment 3 candidate ranking.

The Hard configuration also differs:

- In Setup 1, Hard = B2. It is strongest in that setup and efficient.
- In Setup 2, Hard = B3. It is strongest in the updated setup, but more
  expensive than B2.

Overall, Setup 2 is more coherent with the updated candidate tournament:

```text
Easy   = A1
Medium = B2
Hard   = B3
```

## 10. Conclusion

The recommended final difficulty setup is:

```text
Easy   = A1
Medium = B2
Hard   = B3
```

This recommendation is based on the updated Eval B results and the second
Experiment 4 result set. It preserves a clear difficulty order while assigning
the strongest practical configuration, B3, to Hard.

Important limitation: `result(A1_B2_B3)` has 150 games, while
`result(A1_A3_B2)` has 600 games. If more time is available, the A1/B2/B3 setup
should be rerun with 200 games per pair to match the sample size of the earlier
setup.

## 11. How to Reproduce

Run the tournament:

```bash
python experiments/experiment4_difficulty_tournament/tournament.py
```

Regenerate plots:

```bash
python experiments/experiment4_difficulty_tournament/plot_difficulty_tournament.py
```

Current result folders:

```text
experiments/experiment4_difficulty_tournament/result(A1_A3_B2)
experiments/experiment4_difficulty_tournament/result(A1_B2_B3)
```
