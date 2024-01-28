from typing import Optional

from bitbots_msgs.msg import Utility
from rclpy.logging import get_logger
from rclpy.node import Node

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.state.needs import Needs
from bitbots_body_behavior.state.state import State


class Action:
    def __init__(self, needs: Needs, node: Node):
        self.node = node
        self.needs: list[Needs] = []

        self.topic_base_name = f"debug/body_behavior/{self.__class__.__name__}"
        self.publishers = {}

    @property
    def logger(self):
        return get_logger(self.__class__.__name__)

    def execute(self, blackboard: BodyBlackboard, new_state: Optional[State]):
        raise NotImplementedError

    def evaluate(self, state: State, new_state: Optional[State]) -> float:
        raise NotImplementedError

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return []

    def __repr__(self):
        return self.__class__.__name__

    def create_publisher(self, consideration: str):
        topic_name = f"{self.topic_base_name}/{consideration}"
        self.publishers[consideration] = self.node.create_publisher(Utility, topic_name, 1)

    def publish_consideration_utility(self, consideration: str, utility: float):
        if consideration not in self.publishers:
            self.create_publisher(consideration)

        self.publishers[consideration].publish(Utility(consideration=consideration, utility=utility))
