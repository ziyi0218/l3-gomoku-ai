from dataclasses import dataclass

from ai.evaluation import eval_basic, eval_intermediate
from models import EvalFn


@dataclass(frozen=True)
class AIProfile:
    name: str
    label: str
    evaluation_name: str
    eval_fn: EvalFn
    depth: int
    search: str = "Alpha-Beta + ordering"


DIFFICULTY_AI_PROFILES = [
    AIProfile("Easy", "A1", "Eval A", eval_basic, 1),
    AIProfile("Medium", "A3", "Eval A", eval_basic, 3),
    AIProfile("Hard", "B2", "Eval B", eval_intermediate, 2),
]