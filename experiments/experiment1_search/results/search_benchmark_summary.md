# Experiment 1 Search Benchmark Summary

Fixed evaluation: Eval B / intermediate.
Candidate rule: generate_candidate_moves(radius=2).

|depth|algorithm|ordering|avg_nodes|avg_time_ms|avg_cutoffs|node_reduction_vs_minimax|score_matches_minimax|move_matches_minimax|
|---|---|---|---|---|---|---|---|---|
|1|Alpha-Beta|off|48.6|13.7762|0.0|0.0|5|5|
|1|Alpha-Beta|on|48.6|24.6361|0.0|0.0|5|5|
|1|Minimax|none|48.6|12.3447|0.0|0.0|5|5|
|2|Alpha-Beta|off|573.6|214.8704|44.8|0.7897|5|5|
|2|Alpha-Beta|on|151.6|887.8744|46.2|0.9444|5|4|
|2|Minimax|none|2727.0|875.4747|0.0|0.0|5|5|
|3|Alpha-Beta|off|11555.6|6029.3894|367.0|0.9335|5|5|
|3|Alpha-Beta|on|1782.6|2795.7996|127.2|0.9897|5|4|
|3|Minimax|none|173762.8|71749.5513|0.0|0.0|5|5|
