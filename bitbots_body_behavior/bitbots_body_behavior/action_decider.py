import functools
import itertools
from typing import Iterable, Optional, Tuple

from rclpy.impl.rcutils_logger import RcutilsLogger as Logger

from bitbots_blackboard.blackboard import BodyBlackboard

from .actions import Action, DribbleAction, GoToBallAction, PositioningAction
from .execution.process_pool import ProcessPoolExecutor
from .state.needs import Needs
from .state.state import State

Evaluation = Tuple[Action, list[State]]
EvaluationResult = Tuple[Action, State, float]


class Evaluator:
    def __init__(self, state: State):
        self.state = state

    def evaluate(self, evaluation: Evaluation) -> EvaluationResult:
        results = self.evaluate_new_states(evaluation)
        return max(results, key=lambda item: item[2])

    def evaluate_new_states(self, evaluation: Evaluation) -> Iterable[EvaluationResult]:
        action, new_states = evaluation
        return map(
            lambda state: (action, state, action.evaluate(self.state, state)),
            new_states,
        )


class ActionDecider:
    def __init__(self, blackboard: BodyBlackboard, logger: Logger):
        self.state: State
        self.evaluator: Evaluator
        self.next_action: EvaluationResult
        self.blackboard = blackboard

        self.needs = Needs(self.blackboard)
        self.fulfilled_needs = []
        self.actions: list[Action] = self.setup_actions()
        self.next_action: Optional[EvaluationResult] = None

        self.logger = logger
        self.max_parallel_states = 4
        # max_workers = int(len(ALL_ACTIONS) * self.max_parallel_states / 2)
        self.executor = ProcessPoolExecutor(4)

    def setup_actions(self) -> list[Action]:
        return [
            GoToBallAction(self.needs),
            DribbleAction(self.needs),
            PositioningAction(self.needs),
        ]

    def update_state(self):
        self.state.update()
        self.evaluator = Evaluator(self.state)
        self.fulfilled_needs = self.needs.available()

    def decide(self):
        def flat_map(f, args):
            return functools.reduce(lambda a, b: itertools.chain(a, b), map(f, args))

        self.update_state()

        possible_actions = filter(lambda a: self.fulfilled_needs <= a.needs, self.actions)
        needed_evaluations = flat_map(self.split_into_evaluation_parts, possible_actions)
        split_results = self.parallel_evaluation(needed_evaluations)

        if len(list(split_results)):
            ideal_action = max(split_results, key=lambda item: item[2])
            self.next_action = ideal_action

            self.logger.info(f"Ideal action: {ideal_action[0]}, max_score: {ideal_action[2]}, {ideal_action[1]})")

    def execute_ideal_action(self):
        if self.next_action:
            self.logger.info(f"Executing ideal action: {self.next_action[0]}")
            # self.next_action[0].execute(self.next_action[2])

    def parallel_evaluation(self, evaluations: Iterable[Evaluation]) -> list[EvaluationResult]:
        return self.executor.map(self.evaluator.evaluate, evaluations)

    def synchronous_evaluation(self, evaluations: Iterable[Evaluation]) -> list[EvaluationResult]:
        split_results: list[EvaluationResult] = []

        for action, states in evaluations:
            split_results.append(self.evaluator.evaluate((action, states)))

        return split_results

    def split_into_evaluation_parts(self, action: Action) -> Iterable[Evaluation]:
        new_states = action.next_states_to_evaluate(self.state)
        parts = [
            new_states[i : i + self.max_parallel_states] for i in range(0, len(new_states), self.max_parallel_states)
        ]
        return map(lambda part: (action, part), parts)
