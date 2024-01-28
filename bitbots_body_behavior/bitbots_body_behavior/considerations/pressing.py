from bitbots_body_behavior.actions.action import Action
from bitbots_body_behavior.considerations.consideration import Consideration
from bitbots_body_behavior.considerations.offensive_mapping import OffensiveMapping
from bitbots_body_behavior.functions.combinators import ExponentialDifference
from bitbots_body_behavior.functions.utility_functions import SigmoidUF
from bitbots_body_behavior.state.state import State


class Pressing(Consideration):
    @staticmethod
    def get_utility_value(state: State, action: Action):
        offensive_mapping = OffensiveMapping.get_utility_value(state.role)
        action.publish_consideration_utility("pressing/offensive_mapping", offensive_mapping)

        ball_position_x = SigmoidUF.setup(4).apply(state.ball_position_xy[0])
        action.publish_consideration_utility("pressing/offensive_mapping", ball_position_x)

        utility = ExponentialDifference.apply([offensive_mapping, ball_position_x], 5)
        action.publish_consideration_utility("pressing", utility)

        return utility
