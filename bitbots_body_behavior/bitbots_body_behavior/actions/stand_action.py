from bitbots_msgs.msg import HeadMode
from rclpy.node import Node

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class StandAction(Action):
    def __init__(self, needs: Needs, node: Node):
        super().__init__(needs, node)
        self.needs: list[Need] = []
        self.able_to_move = needs.ABLE_TO_MOVE.available

    def evaluate(self, _: State, new_state: State) -> float:
        if not self.able_to_move() and new_state.head_mode == HeadMode.LOOK_FORWARD:
            return 1.0
        else:
            return 0.0

    def next_states_to_evaluate(self, state: State) -> list[State]:
        used_head_modes = [HeadMode.BALL_MODE, HeadMode.FIELD_FEATURES, HeadMode.LOOK_FORWARD]
        return list(map(state.set_head_mode, used_head_modes))

    def execute(self, blackboard: BodyBlackboard, state: State):
        blackboard.misc.set_head_mode(state.head_mode)
        blackboard.pathfinding.cancel_goal()
        blackboard.pathfinding.stop_walk()
