from bitbots_body_behavior.functions.combinators import(
    Prioritization,
)
from bitbots_body_behavior.functions.utility_functions import (
    LinearUF,
    PiecewiseUF,
)
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State
from bitbots_body_behavior.actions.offensive_mapping import OffensiveMapping

from .action import Action


class DribbleAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, state: State) -> float:
        #Offensive Mapping
        offensive_mapping = OffensiveMapping.apply(state.role)

        # Block 1: Spielsituation
        goal_difference = PiecewiseUF.setup(LinearUF.setup(-1, 8, 0.5), 4, -4).apply(state.goal_difference)
        seconds_remaining = PiecewiseUF.setup(LinearUF.setup(-1, 30, 1), 30, 0).apply(state.seconds_remaining)

        game_pressure = Prioritization.apply([goal_difference, seconds_remaining], [9, 1])
        
        combinator_off_press = Prioritization.apply([offensive_mapping, game_pressure], [4, 6])

        return combinator_off_press

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return []
