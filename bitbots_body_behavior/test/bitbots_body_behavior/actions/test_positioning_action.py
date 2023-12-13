from bitbots_body_behavior.actions import PositioningAction


def test_evalutate(state, new_state, needs):
    action = PositioningAction(needs)
    utility = action.evaluate(state, new_state)

    assert isinstance(utility, float)
    assert utility >= 0.0


def test_next_states_to_evaluate_no_teammates_in_walking_distance(snapshot, needs, state):
    state.current_position = (0, 0, 0)
    state.active_teammate_poses = [(1, 1, 0), (-1, -1, 0)]
    state.set_current_position = lambda x: x

    action = PositioningAction(needs)
    next_states = action.next_states_to_evaluate(state)

    assert len(next_states) == 9
    assert next_states == snapshot


def test_next_states_to_evaluate_teammates_in_walking_distance(snapshot, needs, state):
    state.current_position = (0, 0, 0)
    state.active_teammate_poses = [(0.3, 0.3, 0), (-0.3, 0.3, 0)]
    state.set_current_position = lambda x: x

    action = PositioningAction(needs)
    next_states = action.next_states_to_evaluate(state)

    print(next_states)
    assert len(next_states) == 3
    assert next_states == snapshot
