from unittest.mock import Mock

import pytest
from bitbots_msgs.msg import GameState
from rclpy.impl.rcutils_logger import RcutilsLogger as Logger

from bitbots_body_behavior.action_decider import ActionDecider
from bitbots_body_behavior.actions.go_to_ball_action import GoToBallAction
from bitbots_body_behavior.evaluation import SyncEvaluator
from bitbots_body_behavior.state.needs import Needs


def test_no_needs_fulfilled(decider, blackboard):
    no_needs_fulfilled(blackboard)

    decider.decide()

    assert decider.fulfilled_needs == []
    assert decider.best_result is None


def test_only_able_to_move_need_fulfilled(decider, blackboard):
    no_needs_fulfilled(blackboard)
    blackboard.gamestate.get_gamestate.return_value = GameState.GAMESTATE_PLAYING

    decider.decide()

    assert decider.fulfilled_needs == [decider.needs.ABLE_TO_MOVE]
    assert decider.best_result is None


def test_only_ball_seen_need_fulfilled(decider, blackboard):
    no_needs_fulfilled(blackboard)
    blackboard.world_model.ball_has_been_seen.return_value = True

    decider.decide()

    assert decider.fulfilled_needs == [decider.needs.BALL_SEEN]
    assert decider.best_result is None


def test_able_to_move_and_ball_seen_need_fulfilled(decider, blackboard):
    no_needs_fulfilled(blackboard)
    blackboard.gamestate.get_gamestate.return_value = GameState.GAMESTATE_PLAYING
    blackboard.world_model.ball_has_been_seen.return_value = True

    decider.decide()

    assert decider.fulfilled_needs == [decider.needs.ABLE_TO_MOVE, decider.needs.BALL_SEEN]
    assert isinstance(decider.best_result[0], GoToBallAction)


def no_needs_fulfilled(blackboard):
    # AbleToMoveNeed
    blackboard.gamestate.get_is_penalized.return_value = False
    blackboard.kick.is_currently_kicking = False
    blackboard.gamestate.get_gamestate.return_value = GameState.GAMESTATE_INITIAL

    # BallSeenNeed
    blackboard.world_model.ball_has_been_seen.return_value = False


@pytest.fixture
def decider(blackboard, state, logger) -> ActionDecider:
    return ActionDecider(blackboard, state, Needs(blackboard), SyncEvaluator(), logger)


@pytest.fixture
def logger():
    logger = Mock(Logger)
    logger.info = print

    return logger
