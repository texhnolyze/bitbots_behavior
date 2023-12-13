from unittest.mock import Mock

import pytest
from bitbots_msgs.msg import HeadMode, Strategy
from geometry_msgs.msg import Point, Pose, Quaternion

from bitbots_blackboard.blackboard import BodyBlackboard, GameStatusCapsule, KickCapsule, MiscCapsule, WorldModelCapsule, TeamDataCapsule
from bitbots_body_behavior.state.needs import AbleToMoveNeed, ClosestToBallNeed, BallSeenNeed, Needs
from bitbots_body_behavior.state.state import State


@pytest.fixture
def blackboard() -> BodyBlackboard:
    blackboard: BodyBlackboard = Mock(BodyBlackboard)

    blackboard.gamestate = Mock(GameStatusCapsule)
    blackboard.kick = Mock(KickCapsule)
    blackboard.world_model = Mock(WorldModelCapsule)
    blackboard.misc = Mock(MiscCapsule)
    blackboard.team_data = Mock(TeamDataCapsule)

    return blackboard


@pytest.fixture
def state(new_state) -> State:
    state: State = Mock(State)
    state.update.return_value = state
    state.set_head_mode.return_value = new_state

    state.role = [Strategy.ROLE_SUPPORTER, 10000000]
    state.goal_difference = 0
    state.seconds_remaining = 120.0
    state.current_position = [1.0, 1.0, 0.2]
    state.distance_to_ball = 1.2
    state.ball_position_xy = [3.4, 5.6]
    state.angle_to_ball = 5.6
    state.time_to_ball = 7.8

    return state


@pytest.fixture
def new_state() -> State:
    state: State = Mock(State)
    state.head_mode = HeadMode.DONT_MOVE

    return state


@pytest.fixture
def needs():
    needs = Mock(Needs)
    needs.ABLE_TO_MOVE = Mock(AbleToMoveNeed)
    needs.BALL_SEEN = Mock(BallSeenNeed)
    needs.CLOSEST_TO_BALL = Mock(ClosestToBallNeed)

    return needs


def base_pose() -> Pose:
    point = Point(x=3.6, y=1.8, z=1.9)
    quat = Quaternion(x=0.2, y=0.3, z=0.5, w=0.8)

    return Pose(position=point, orientation=quat)
