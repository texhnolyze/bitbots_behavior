from typing import Optional

import rclpy

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.state.needs import Needs
from bitbots_body_behavior.state.state import State


class Action:
    def __init__(self, needs: Needs):
        self.needs: list[Needs] = []

    @property
    def logger(self):
        return rclpy.logging.get_logger(self.__class__.__name__)

    def execute(self, blackboard: BodyBlackboard, new_state: Optional[State]):
        raise NotImplementedError

    def evaluate(self, state: State, new_state: Optional[State]) -> float:
        raise NotImplementedError

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return []

    def __repr__(self):
        return self.__class__.__name__
