from bitbots_body_behavior.considerations.consideration import Consideration
from bitbots_body_behavior.considerations.offensive_mapping import OffensiveMapping
from bitbots_body_behavior.functions.combinators import ExponentialDifference
from bitbots_body_behavior.functions.utility_functions import SigmoidUF
from bitbots_body_behavior.state.state import State


class Pressing(Consideration):
    @staticmethod
    def get_utility_value(state: State):
        offensive_mapping = OffensiveMapping.get_utility_value(state.role)
        ball_position_x = SigmoidUF.setup(4).apply(state.ball_position_xy[0])
        return ExponentialDifference.apply([offensive_mapping, ball_position_x], 5)
