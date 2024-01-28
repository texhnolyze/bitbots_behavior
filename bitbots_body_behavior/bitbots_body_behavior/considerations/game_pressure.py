from bitbots_body_behavior.actions.action import Action
from bitbots_body_behavior.considerations.consideration import Consideration
from bitbots_body_behavior.functions.combinators import Prioritization
from bitbots_body_behavior.functions.utility_functions import LinearUF, PiecewiseUF
from bitbots_body_behavior.state.state import State


class GamePressure(Consideration):
    @staticmethod
    def get_utility_value(state: State, action: Action):
        goal_difference = PiecewiseUF.setup(LinearUF.setup(-1, 8, 0.5), 4, -4).apply(state.goal_difference)
        action.publish_consideration_utility("game_pressure/goal_difference", goal_difference)

        seconds_remaining = PiecewiseUF.setup(LinearUF.setup(-1, 30, 1), 30, 0).apply(state.seconds_remaining)
        action.publish_consideration_utility("game_pressure/seconds_remaining", seconds_remaining)

        utility = Prioritization.apply([goal_difference, seconds_remaining], [9, 1])
        action.publish_consideration_utility("game_pressure", utility)

        return utility
