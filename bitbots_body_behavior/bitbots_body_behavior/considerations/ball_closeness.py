from bitbots_body_behavior.actions.action import Action
from bitbots_body_behavior.considerations.consideration import Consideration
from bitbots_body_behavior.functions.combinators import AndCombinator
from bitbots_body_behavior.functions.utility_functions import EulerExponentialUF, NormVerteilungUF
from bitbots_body_behavior.state.state import State


class BallCloseness(Consideration):
    @staticmethod
    def get_utility_value(state: State, action: Action):
        ball_angle = NormVerteilungUF.setup(sigma=0.4).apply(state.angle_to_ball)
        action.publish_consideration_utility("ball_closeness/ball_angle", ball_angle)

        ball_distance = EulerExponentialUF.setup(exponent_factor=-0.5).apply(state.distance_to_ball)
        action.publish_consideration_utility("ball_closeness/ball_distance", ball_distance)

        utility = AndCombinator.apply([ball_angle, ball_distance])
        action.publish_consideration_utility("ball_closeness", utility)
        return utility
