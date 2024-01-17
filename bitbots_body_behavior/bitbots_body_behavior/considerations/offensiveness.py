from bitbots_msgs.msg import Strategy

from bitbots_body_behavior.considerations.consideration import Consideration
from bitbots_body_behavior.functions.combinators import AndCombinator
from bitbots_body_behavior.functions.utility_functions import SigmoidTwoXUF
from bitbots_body_behavior.state.state import State


class Offensiveness(Consideration):
    @staticmethod
    def get_utility_value(new_state: State):
        if new_state.role != Strategy.ROLE_STRIKER:
            return 0

        x_distance_to_opponent_goal = SigmoidTwoXUF.setup(15, 1.75, 1, 1, -1).apply(
            new_state.map_based_opp_goal_center_xy[0] - new_state.current_position[0]
        )
        x_distance_to_opponent_goal = min(x_distance_to_opponent_goal, 1)
        y_distance_to_opponent_goal = SigmoidTwoXUF.setup(2, 2).apply(new_state.current_position[1])

        return AndCombinator.apply([x_distance_to_opponent_goal, y_distance_to_opponent_goal])
