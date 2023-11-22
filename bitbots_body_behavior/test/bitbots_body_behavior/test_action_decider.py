from unittest.mock import Mock

import pytest
from bitbots_msgs.msg import GameState
from geometry_msgs.msg import Point, Pose, Quaternion
from rclpy.impl.rcutils_logger import RcutilsLogger as Logger

from bitbots_blackboard.blackboard import BodyBlackboard, GameStatusCapsule, KickCapsule
from bitbots_body_behavior.action_decider import ActionDecider
from bitbots_body_behavior.actions import Action
from bitbots_body_behavior.evaluation import Evaluator, SyncEvaluator
from bitbots_body_behavior.state.needs import Needs
from bitbots_body_behavior.state.state import State


def test_setup_of_action_decider(blackboard, state, evaluator, logger):
    decider = ActionDecider(blackboard, state, evaluator, logger)

    assert decider.blackboard == blackboard
    assert decider.state == state
    assert decider.logger == logger
    assert len(decider.actions) > 0
    assert isinstance(decider.needs, Needs)
    assert decider.fulfilled_needs == []
    assert decider.next_action is None


def test_decide_action(decider, state):
    decider.decide()

    assert state.update.called
    assert decider.next_action is not None
    assert isinstance(decider.next_action[0], Action)
    assert isinstance(decider.next_action[1], State)
    assert isinstance(decider.next_action[2], float)


# def test_something(blackboard):
#     state = State(blackboard)
#     state.seconds_remaining = 10
#     new_state = state.copy()

#     print(hex(id(state)))
#     print(hex(id(new_state)))

#     print(hex(id(state.seconds_remaining)))
#     print(hex(id(new_state.seconds_remaining)))


@pytest.fixture
def decider(blackboard, state, logger) -> ActionDecider:
    return ActionDecider(blackboard, state, SyncEvaluator(), logger)


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


@pytest.fixture
def blackboard() -> BodyBlackboard:
    blackboard: BodyBlackboard = Mock(BodyBlackboard)

    blackboard.gamestate = Mock(GameStatusCapsule)
    blackboard.gamestate.get_gamestate.return_value = GameState.GAMESTATE_PLAYING
    blackboard.gamestate.get_is_penalized.return_value = False

    blackboard.kick = Mock(KickCapsule)
    blackboard.kick.is_currently_kicking = False

    return blackboard


@pytest.fixture
def state() -> State:
    state: State = Mock(State)
    state.update.return_value = state

    state.current_position = base_pose()
    state.distance_to_ball = 1.2
    state.ball_position_xy = Point(x=1.2, y=3.4)
    state.angle_to_ball = 5.6
    state.time_to_ball = 7.8

    return state


def base_pose() -> Pose:
    point = Point(x=3.6, y=1.8, z=1.9)
    quat = Quaternion(x=0.2, y=0.3, z=0.5, w=0.8)

    return Pose(position=point, orientation=quat)
