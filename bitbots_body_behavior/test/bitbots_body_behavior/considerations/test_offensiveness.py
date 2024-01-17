from bitbots_msgs.msg import Strategy

from bitbots_body_behavior.considerations.offensiveness import Offensiveness


def test_max_offensiveness(state):
    state.role = Strategy.ROLE_STRIKER
    state.current_position = (3.0, 0.0, 0.0)

    utility = Offensiveness.get_utility_value(state)
    assert utility == 1.0


def test_min_offensiveness(state):
    state.role = Strategy.ROLE_DEFENDER
    state.current_position = (-3.0, 0.0, 0.0)

    utility = Offensiveness.get_utility_value(state)
    assert utility == 0.0


def test_x_position_offensiveness(state):
    state.role = Strategy.ROLE_STRIKER

    state.current_position = (2.5, 0.0, 0.0)
    utility = Offensiveness.get_utility_value(state)
    assert utility > 0.5

    state.current_position = (3.5, 0.0, 0.0)
    utility = Offensiveness.get_utility_value(state)
    assert utility > 0.5


def test_y_position_offensiveness(state):
    state.role = Strategy.ROLE_STRIKER

    state.current_position = (3.0, 1.0, 0.0)
    utility = Offensiveness.get_utility_value(state)
    assert utility > 0.5

    state.current_position = (3.0, -1.0, 0.0)
    utility = Offensiveness.get_utility_value(state)
    assert utility > 0.5
