from bitbots_body_behavior.actions.stand_action import StandAction


def test_evalutate_moving_allowed(state, needs):
    needs.ABLE_TO_MOVE.available.return_value = True

    action = StandAction(needs)
    utility = action.evaluate(state)

    assert isinstance(utility, float)
    assert utility == 0.0


def test_evalutate_moving_not_allowed(state, needs):
    needs.ABLE_TO_MOVE.available.return_value = False

    action = StandAction(needs)
    utility = action.evaluate(state)

    assert isinstance(utility, float)
    assert utility == 1.0
