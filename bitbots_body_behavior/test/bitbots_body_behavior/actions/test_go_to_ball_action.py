from bitbots_body_behavior.actions.go_to_ball_action import GoToBallAction


def test_evalutate(state, needs):
    action = GoToBallAction(needs)
    utility = action.evaluate(state)

    assert isinstance(utility, float)
    assert utility >= 0.0
