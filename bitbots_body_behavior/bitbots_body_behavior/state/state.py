from copy import copy
from typing import Tuple

from bitbots_blackboard.blackboard import BodyBlackboard


class State:
    def __init__(self, blackboard: BodyBlackboard) -> None:
        self.blackboard = blackboard

    def update(self) -> None:
        # own properties
        self.current_position = self.blackboard.world_model.get_current_position()
        self.head_mode = self.blackboard.misc.get_head_mode()

        # ball properties
        self.distance_to_ball = self.blackboard.world_model.get_ball_distance()
        self.ball_position_xy = self.blackboard.world_model.get_ball_position_xy()
        self.angle_to_ball = self.blackboard.world_model.get_ball_angle()
        self.time_to_ball = self.blackboard.pathfinding.calculate_time_to_ball()

        # opponent goal properties
        self.map_based_opp_goal_distance = self.blackboard.world_model.get_map_based_opp_goal_distance()
        self.map_based_opp_goal_center_uv = self.blackboard.world_model.get_map_based_opp_goal_center_uv()
        self.map_based_opp_goal_center_xy = self.blackboard.world_model.get_map_based_opp_goal_center_xy()
        self.map_based_own_goal_center_uv = self.blackboard.world_model.get_map_based_own_goal_center_uv()
        self.map_based_own_goal_center_xy = self.blackboard.world_model.get_map_based_own_goal_center_xy()

        # gamestate properties
        self.role = self.blackboard.team_data.get_role()
        self.own_goals = self.blackboard.gamestate.get_own_goals()
        self.goal_difference = self.blackboard.gamestate.get_goal_difference()
        self.seconds_remaining = self.blackboard.gamestate.get_seconds_remaining()
        self.red_cards = self.blackboard.gamestate.get_red_cards()

        # additional properties
        self.active_teammate_poses = self.blackboard.team_data.get_active_teammate_poses()
        self.rank_to_ball = self.blackboard.team_data.team_rank_to_ball(self.distance_to_ball)

        # Potentially interesting for future states
        # self.get_ball_goal = blackboard.pathfinding.get_ball_goal(BallGoalType.MAP)
        # self.time_from_pose_to_pose = blackboard.pathfinding.time_from_pose_to_pose()

    def copy(self) -> "State":
        instance = copy(self)
        del instance.blackboard
        return instance

    def set_head_mode(self, head_mode: int) -> "State":
        instance = copy(self)
        instance.head_mode = head_mode
        return instance

    def set_current_position(self, current_position: Tuple[float, float, float]) -> "State":
        instance = copy(self)
        instance.current_position = current_position
        return instance
