from typing import Optional

from rclpy.impl.rcutils_logger import RcutilsLogger as Logger

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.evaluation import Evaluation, EvaluationResult, Evaluator

from .actions import Action, DribbleAction, GoToBallAction, StandAction
from .state.needs import Needs
from .state.state import State


class ActionDecider:
    def __init__(
        self,
        blackboard: BodyBlackboard,
        state: State,
        needs: Needs,
        evaluator: Evaluator,
        logger: Logger,
    ):
        self.blackboard = blackboard
        self.state = state
        self.needs = needs
        self.evaluator = evaluator

        self.fulfilled_needs = []
        self.actions: list[Action] = self.setup_actions()
        self.best_result: Optional[EvaluationResult] = None

        self.logger = logger
        self.max_parallel_states = 4

    def setup_actions(self) -> list[Action]:
        return [
            StandAction(self.needs),
            GoToBallAction(self.needs),
            DribbleAction(self.needs),
            # PositioningAction(self.needs),
        ]

    def update_state(self):
        self.state.update()
        self.fulfilled_needs = self.needs.available()

    def decide(self):
        self.update_state()

        possible_actions = list(filter(self.are_actions_needs_fulfilled, self.actions))
        if len(possible_actions) == 0:
            self.best_result = None
        else:
            needed_evaluations = list(map(self.evaluation_from_action, possible_actions))
            results = list(self.evaluator.evaluate_actions(needed_evaluations))

            if len(results):
                ideal_action = max(results, key=lambda item: item[2])
                self.best_result = ideal_action
                self.logger.info(
                    f"Best action: {ideal_action[0]}, utility: {ideal_action[2]}, new_state: {ideal_action[1]})"
                )

    def execute_ideal_action(self):
        if self.best_result:
            action, new_state, utility_value = self.best_result
            action.execute(self.blackboard, new_state)

    def evaluation_from_action(self, action: Action) -> Evaluation:
        next_states = action.next_states_to_evaluate(self.state)

        return (action, self.state, next_states)

    def are_actions_needs_fulfilled(self, action: Action) -> bool:
        return all(need in self.fulfilled_needs for need in action.needs)
