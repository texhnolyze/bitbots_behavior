from bitbots_msgs.msg import HeadMode

from bitbots_body_behavior.actions.stand_action import StandAction


def test_next_states_to_evaluate(needs, state):
    action = StandAction(needs)
    next_states = action.next_states_to_evaluate(state)

    assert state.set_head_mode.called_with(HeadMode.BALL_MODE, HeadMode.FIELD_FEATURES, HeadMode.LOOK_FORWARD)
    assert len(next_states) == 3


def test_evalutate_moving_allowed(state, new_state, needs):
    needs.ABLE_TO_MOVE.available.return_value = True

    action = StandAction(needs)
    utility = action.evaluate(state, new_state)

    assert isinstance(utility, float)
    assert utility == 0.0


def test_evalutate_moving_not_allowed_looking_forward(state, new_state, needs):
    needs.ABLE_TO_MOVE.available.return_value = False
    new_state.head_mode = HeadMode.LOOK_FORWARD

    action = StandAction(needs)
    utility = action.evaluate(state, new_state)

    assert isinstance(utility, float)
    assert utility == 1.0


def test_evalutate_moving_not_allowed_looking_for_ball(state, new_state, needs):
    needs.ABLE_TO_MOVE.available.return_value = False
    new_state.head_mode = HeadMode.BALL_MODE

    action = StandAction(needs)
    utility = action.evaluate(state, new_state)

    assert isinstance(utility, float)
    assert utility == 0.0
