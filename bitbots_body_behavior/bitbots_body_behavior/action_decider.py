import functools
import itertools
from typing import Iterable, Optional

from rclpy.impl.rcutils_logger import RcutilsLogger as Logger

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.evaluation import Evaluation, EvaluationResult, Evaluator

from .actions import Action, DribbleAction, GoToBallAction, PositioningAction
from .state.needs import Needs
from .state.state import State


class ActionDecider:
    def __init__(
        self,
        blackboard: BodyBlackboard,
        state: State,
        evaluator: Evaluator,
        logger: Logger,
    ):
        self.blackboard = blackboard
        self.state = state
        self.evaluator = evaluator

        self.needs = Needs(self.blackboard)
        self.fulfilled_needs = []
        self.actions: list[Action] = self.setup_actions()
        self.next_action: Optional[EvaluationResult] = None

        self.logger = logger
        self.max_parallel_states = 4

    def setup_actions(self) -> list[Action]:
        return [
            GoToBallAction(self.needs),
            DribbleAction(self.needs),
            PositioningAction(self.needs),
        ]

    def update_state(self):
        self.state.update()
        self.fulfilled_needs = self.needs.available()

    def decide(self):
        def flat_map(f, args):
            return functools.reduce(lambda a, b: itertools.chain(a, b), map(f, args))

        self.update_state()

        possible_actions = filter(lambda a: self.fulfilled_needs <= a.needs, self.actions)

        needed_evaluations = flat_map(self.split_into_evaluation_parts, possible_actions)
        split_results = list(self.evaluator.evaluate_actions(needed_evaluations))

        if len(split_results):
            ideal_action = max(split_results, key=lambda item: item[2])
            self.next_action = ideal_action

            self.logger.info(f"Ideal action: {ideal_action[0]}, max_score: {ideal_action[2]}, {ideal_action[1]})")

    def execute_ideal_action(self):
        if self.next_action:
            self.logger.info(f"Executing ideal action: {self.next_action[0]}")
            # self.next_action[0].execute(self.next_action[2])

    def split_into_evaluation_parts(self, action: Action) -> Iterable[Evaluation]:
        new_states = action.next_states_to_evaluate(self.state)
        parts = [
            new_states[i : i + self.max_parallel_states] for i in range(0, len(new_states), self.max_parallel_states)
        ]
        return map(lambda part: (action, self.state, part), parts)
