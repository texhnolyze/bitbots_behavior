from unittest.mock import Mock

import pytest
from bitbots_msgs.msg import GameState
from rclpy.impl.rcutils_logger import RcutilsLogger as Logger

from bitbots_body_behavior.action_decider import ActionDecider
from bitbots_body_behavior.actions.go_to_ball_action import GoToBallAction
from bitbots_body_behavior.evaluation import SyncEvaluator
from bitbots_body_behavior.state.needs import Needs


def test_able_to_move_need_fulfilled(decider, blackboard):
    blackboard.gamestate.get_is_penalized.return_value = False
    blackboard.gamestate.get_gamestate.return_value = GameState.GAMESTATE_PLAYING
    blackboard.kick.is_currently_kicking = False

    decider.decide()

    assert decider.fulfilled_needs == [decider.needs.ABLE_TO_MOVE]
    assert isinstance(decider.best_result[0], GoToBallAction)


def test_able_to_move_need_not_fulfilled(decider, blackboard):
    blackboard.gamestate.get_is_penalized.return_value = False
    blackboard.gamestate.get_gamestate.return_value = GameState.GAMESTATE_SET
    blackboard.kick.is_currently_kicking = False

    decider.decide()

    assert decider.fulfilled_needs == []
    assert decider.best_result is None


@pytest.fixture
def decider(blackboard, state, logger) -> ActionDecider:
    return ActionDecider(blackboard, state, Needs(blackboard), SyncEvaluator(), logger)


@pytest.fixture
def logger():
    logger = Mock(Logger)
    logger.info = print

    return logger
