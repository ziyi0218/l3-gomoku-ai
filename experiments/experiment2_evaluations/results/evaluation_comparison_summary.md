# Experiment 2 Evaluation Comparison Summary

This is a fresh rerun after Eval A was modified.
Search: Alpha-Beta + move ordering.
Depths: 1, 2, 3.
Candidate rule: generate_candidate_moves(radius=2).

|depth|evaluation|positions|avg_time_ms|avg_nodes|avg_cutoffs|avg_candidate_count|
|---|---|---|---|---|---|---|
|1|Eval A|6|37.7455|58.0|0.0|57.0|
|1|Eval B|6|27.2856|58.0|0.0|57.0|
|1|Eval C|6|245.874|58.0|0.0|57.0|
|2|Eval A|6|1316.8133|190.5|55.67|57.0|
|2|Eval B|6|903.7211|224.0|55.17|57.0|
|2|Eval C|6|8244.916|209.5|55.33|57.0|
|3|Eval A|6|6152.1513|4196.17|145.5|57.0|
|3|Eval B|6|4549.0734|4120.17|151.0|57.0|
|3|Eval C|6|35588.1905|4151.83|136.67|57.0|
