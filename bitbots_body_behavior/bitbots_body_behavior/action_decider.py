from typing import Optional

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
            # DribbleAction(self.needs),
            # PositioningAction(self.needs),
        ]

    def update_state(self):
        self.state.update()
        self.fulfilled_needs = self.needs.available()

    def decide(self):
        self.update_state()

        possible_actions = list(filter(self.are_actions_needs_fulfilled, self.actions))
        needed_evaluations = list(map(self.evaluation_from_action, possible_actions))
        results = list(self.evaluator.evaluate_actions(needed_evaluations))

        if len(results):
            ideal_action = max(results, key=lambda item: item[2])
            self.next_action = ideal_action

            self.logger.info(f"Ideal action: {ideal_action[0]}, max_score: {ideal_action[2]}, {ideal_action[1]})")

    def execute_ideal_action(self):
        if self.next_action:
            self.logger.info(f"Executing ideal action: {self.next_action[0]}")
            self.next_action[0].execute(self.blackboard, self.next_action[2])

    def evaluation_from_action(self, action: Action) -> Evaluation:
        print(f"evaluation from action: {action}")
        next_states = action.next_states_to_evaluate(self.state)

        return (action, self.state, next_states)

    def are_actions_needs_fulfilled(self, action: Action) -> bool:
        print(f"filter: {all(need in self.fulfilled_needs for need in action.needs)}")
        return all(need in self.fulfilled_needs for need in action.needs)
