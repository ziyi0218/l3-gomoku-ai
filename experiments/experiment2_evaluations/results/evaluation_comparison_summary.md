# Experiment 2 Evaluation Comparison Summary

Search: Alpha-Beta + move ordering.
Depths: 1, 2, 3.
Candidate rule: generate_candidate_moves(radius=2).

|depth|evaluation|positions|avg_time_ms|avg_nodes|avg_cutoffs|avg_candidate_count|
|---|---|---|---|---|---|---|
|1|Eval A|5|42.7976|54.6|0.0|53.6|
|1|Eval B|5|48.0968|54.6|0.0|53.6|
|1|Eval C|5|492.8529|54.6|0.0|53.6|
|2|Eval A|5|1404.0459|162.8|52.6|53.6|
|2|Eval B|5|1712.4998|194.2|52.0|53.6|
|2|Eval C|5|15368.7781|206.8|51.8|53.6|
|3|Eval A|5|5932.5626|3593.6|107.2|53.6|
|3|Eval B|5|7665.048|3590.6|117.6|53.6|
|3|Eval C|5|63505.0764|3607.2|118.6|53.6|
