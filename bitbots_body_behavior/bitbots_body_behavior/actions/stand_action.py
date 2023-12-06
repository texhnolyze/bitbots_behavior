from typing import Optional

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class StandAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = []
        self.able_to_move = needs.ABLE_TO_MOVE.available

    def evaluate(self, state: State) -> float:
        if not self.able_to_move():
            return 1.0
        else:
            return 0.0

    def execute(self, blackboard: BodyBlackboard, _: Optional[State]):
        blackboard.pathfinding.cancel_goal()
        blackboard.pathfinding.stop_walk()
