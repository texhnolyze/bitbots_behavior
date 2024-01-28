from bitbots_msgs.msg import Strategy

from bitbots_body_behavior.actions.action import Action
from bitbots_body_behavior.considerations.consideration import Consideration
from bitbots_body_behavior.functions.combinators import AndCombinator
from bitbots_body_behavior.functions.utility_functions import SigmoidTwoXUF
from bitbots_body_behavior.state.state import State


class Defensiveness(Consideration):
    @staticmethod
    def get_utility_value(new_state: State, action: Action):
        if new_state.role != Strategy.ROLE_DEFENDER:
            return 0

        x_distance_to_own_goal = SigmoidTwoXUF.setup(15, 1.75, 1, 1, -1).apply(
            new_state.current_position[0] - new_state.map_based_own_goal_center_xy[0]
        )
        x_distance_to_own_goal = min(x_distance_to_own_goal, 1)
        action.publish_consideration_utility("defensiveness/x_distance_to_own_goal", x_distance_to_own_goal)

        y_distance_to_own_goal = SigmoidTwoXUF.setup(2, 2).apply(new_state.current_position[1])
        action.publish_consideration_utility("defensiveness/y_distance_to_own_goal", y_distance_to_own_goal)

        utility = AndCombinator.apply([x_distance_to_own_goal, y_distance_to_own_goal])
        action.publish_consideration_utility("defensiveness", utility)

        return utility
