from bitbots_body_behavior.considerations.consideration import Consideration
from bitbots_body_behavior.functions.combinators import Prioritization
from bitbots_body_behavior.functions.utility_functions import LinearUF, PiecewiseUF
from bitbots_body_behavior.state.state import State


class GamePressure(Consideration):
    @staticmethod
    def get_utility_value(state: State):
        goal_difference = PiecewiseUF.setup(LinearUF.setup(-1, 8, 0.5), 4, -4).apply(state.goal_difference)
        seconds_remaining = PiecewiseUF.setup(LinearUF.setup(-1, 30, 1), 30, 0).apply(state.seconds_remaining)
        return Prioritization.apply([goal_difference, seconds_remaining], [9, 1])
