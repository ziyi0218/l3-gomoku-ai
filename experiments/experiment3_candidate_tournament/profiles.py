from dataclasses import dataclass

from ai.evaluation import eval_advanced, eval_basic, eval_intermediate
from models import EvalFn


@dataclass(frozen=True)
class AIProfile:
    name: str
    evaluation_name: str
    eval_fn: EvalFn
    depth: int
    search: str = "Alpha-Beta + ordering"


CANDIDATE_AI_PROFILES = [
    AIProfile("A1", "Eval A", eval_basic, 1),
    AIProfile("B1", "Eval B", eval_intermediate, 1),
    AIProfile("A2", "Eval A", eval_basic, 2),
    AIProfile("B2", "Eval B", eval_intermediate, 2),
    AIProfile("C2", "Eval C", eval_advanced, 2),
    AIProfile("A3", "Eval A", eval_basic, 3),
    AIProfile("B3", "Eval B", eval_intermediate, 3),
]


EXCLUDED_PROFILES = {
    "C1": "Eval C + depth 1 is excluded because depth 1 is too shallow to show Eval C's five-window potential.",
    "C3": "Eval C + depth 3 is excluded because Experiment 2 showed excessive per-move runtime.",
}
