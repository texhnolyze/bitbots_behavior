from bitbots_body_behavior.functions.combinators import AndCombinator, NaturalLogarithm, OrCombinator, Prioritization
from bitbots_body_behavior.functions.utility_functions import (
    EulerExponentialUF,
    ExponentialUF,
    LinearUF,
    NormVerteilungUF,
    PiecewiseUF,
)
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class GoToBallAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, state: State) -> float:
        # Block1 der Rolle und allgemeinen Ballposition
        offensive_mapping = PiecewiseUF.setup(LinearUF.setup(0, 0), 0.5, 0.5)
        ball_position = ExponentialUF.setup(1, 1, 1)
        combinator_eins = NaturalLogarithm.apply([offensive_mapping, ball_position], 5)

        # Block2 Winkel und Distanz
        ball_angle = NormVerteilungUF.setup(0.25)
        ball_distance = EulerExponentialUF.setup(1, -1, 1)
        combinator_zwei = AndCombinator.apply(
            [ball_angle.apply(self, state.angle_to_ball), ball_distance.apply(self, state.distance_to_ball)]
        )

        combinator_b1_b2 = Prioritization.apply([combinator_eins, combinator_zwei], [2, 8])

        # Block3 Spielsituation
        goal_difference = PiecewiseUF.setup(LinearUF.setup(-1, 8, 0.5), 4, -4)
        seconds_remaining = PiecewiseUF.setup(LinearUF.setup(-1, 30, 1), 30, 0)
        combinator_drei = Prioritization.apply([goal_difference, seconds_remaining], [9, 1])

        return OrCombinator.apply([combinator_b1_b2, combinator_drei])

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return []
