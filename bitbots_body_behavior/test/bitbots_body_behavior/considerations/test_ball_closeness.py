import math

from bitbots_body_behavior.considerations.ball_closeness import BallCloseness


def test_max_ball_closeness(state):
    state.angle_to_ball = 0.0
    state.distance_to_ball = 0.0

    utility = BallCloseness.get_utility_value(state)
    assert utility == 1.0


def test_ball_closeness_angle(state):
    state.distance_to_ball = 0.0

    state.angle_to_ball = math.pi / 4
    utility_90 = BallCloseness.get_utility_value(state)

    state.angle_to_ball = -math.pi / 4
    utility_minus_90 = BallCloseness.get_utility_value(state)

    state.angle_to_ball = math.pi / 8
    utility_45 = BallCloseness.get_utility_value(state)

    assert utility_90 < 0.5
    assert utility_minus_90 == utility_90
    assert utility_45 > 0.5


def test_ball_closeness_distance(state):
    state.angle_to_ball = 0.0

    state.distance_to_ball = 0
    utility_no_distance = BallCloseness.get_utility_value(state)

    state.distance_to_ball = 1
    utility_small_distance = BallCloseness.get_utility_value(state)

    state.distance_to_ball = 2
    utility_large_distance = BallCloseness.get_utility_value(state)

    print(utility_no_distance, utility_small_distance, utility_large_distance)

    assert utility_no_distance == 1.0
    assert utility_large_distance < 0.5
    assert utility_small_distance > 0.5
