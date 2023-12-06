from unittest.mock import Mock

import pytest
from rclpy.impl.rcutils_logger import RcutilsLogger as Logger

from bitbots_body_behavior.action_decider import ActionDecider
from bitbots_body_behavior.evaluation import Evaluator
from bitbots_body_behavior.state.needs import Needs
from bitbots_body_behavior.state.state import State


def test_setup_of_action_decider(blackboard, state, needs, evaluator, logger):
    decider = ActionDecider(blackboard, state, needs, evaluator, logger)

    assert decider.blackboard == blackboard
    assert decider.state == state
    assert decider.needs == needs
    assert decider.logger == logger
    assert len(decider.actions) > 0
    assert isinstance(decider.needs, Needs)
    assert decider.fulfilled_needs == []
    assert decider.best_result is None


def test_decide_updates_state(decider, state, needs):
    needs.available.return_value = [needs.ABLE_TO_MOVE]

    decider.decide()

    state.update.assert_called_once()
    assert decider.fulfilled_needs == [needs.ABLE_TO_MOVE]


def test_decide_evaluates_actions(decider, state, needs, evaluator):
    random_action = Mock()
    random_action.needs = ["some other need"]

    new_states = [Mock(State), Mock(State)]
    positioning_action = Mock()
    positioning_action.needs = [needs.ABLE_TO_MOVE]
    positioning_action.next_states_to_evaluate.return_value = new_states

    needs.available.return_value = [needs.ABLE_TO_MOVE]

    decider.actions = [random_action, positioning_action]
    decider.decide()

    evaluator.evaluate_actions.assert_called_with([(positioning_action, state, new_states)])
    assert evaluator.evaluate_actions.call_count == 1


def test_decide_sets_best_result(decider, state, needs, evaluator):
    random_action = Mock()
    random_action.needs = []
    positioning_action = Mock()
    positioning_action.needs = []
    evaluator.evaluate_actions.return_value = [(random_action, None, 0.1), (positioning_action, None, 0.2)]

    decider.actions = [random_action, positioning_action]
    decider.decide()

    assert decider.best_result == (positioning_action, None, 0.2)


@pytest.fixture
def decider(blackboard, state, needs, evaluator, logger) -> ActionDecider:
    return ActionDecider(blackboard, state, needs, evaluator, logger)


@pytest.fixture
def logger():
    logger = Mock(Logger)
    logger.info = print

    return logger


@pytest.fixture
def evaluator() -> Evaluator:
    evaluator: Evaluator = Mock(Evaluator)
    evaluator.evaluate_actions.return_value = []

    return evaluator
