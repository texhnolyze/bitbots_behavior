from typing import Tuple

from bitbots_msgs.msg import Strategy


class OffensiveMapping:
    @staticmethod
    def apply(role_update: Tuple[int, float]) -> float:
        # Schaut man auf get_role im blackboard, werden diese als Tuple gespeichert,
        # wobei der int für die entsprechende Rolle steht
        role, _ = role_update

        if role == Strategy.ROLE_STRIKER:
            return 0.8
        elif role == Strategy.ROLE_DEFENDER:
            return 0.3
        elif role == Strategy.ROLE_GOALIE:
            return 0.1
        else:
            return 0.0
