# Experiment 2 Evaluation Comparison Summary

This is a fresh rerun after Eval A was modified.
Search: Alpha-Beta + move ordering.
Depths: 1, 2, 3.
Candidate rule: generate_candidate_moves(radius=2).

|depth|evaluation|positions|avg_time_ms|avg_nodes|avg_cutoffs|avg_candidate_count|
|---|---|---|---|---|---|---|
|1|Eval A|6|35.2078|58.0|0.0|57.0|
|1|Eval B|6|24.8029|58.0|0.0|57.0|
|1|Eval C|6|245.8648|58.0|0.0|57.0|
|2|Eval A|6|1353.6469|190.5|55.67|57.0|
|2|Eval B|6|943.3087|211.33|55.33|57.0|
|2|Eval C|6|8657.382|209.5|55.33|57.0|
|3|Eval A|6|6419.806|4196.17|145.5|57.0|
|3|Eval B|6|4527.5326|4154.17|150.5|57.0|
|3|Eval C|6|37228.8886|4151.83|136.67|57.0|
