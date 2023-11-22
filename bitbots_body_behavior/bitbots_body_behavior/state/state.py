from bitbots_blackboard.blackboard import BodyBlackboard


class State:
    def __init__(self, blackboard: BodyBlackboard) -> None:
        self.distance_to_ball = blackboard.world_model.get_ball_distance()
        self.angle_to_ball = blackboard.world_model.get_ball_angle()
        self.ball_position_xy = blackboard.world_model.get_ball_position_xy()
        self.get_map_based_opp_goal_center_uv = blackboard.world_model.get_map_based_opp_goal_center_uv()
        self.get_map_based_opp_goal_center_xy = blackboard.world_model.get_map_based_opp_goal_center_xy()
        self.get_map_based_own_goal_center_uv = blackboard.world_model.get_map_based_own_goal_center_uv()
        self.get_map_based_own_goal_center_xy = blackboard.world_model.get_map_based_own_goal_center_xy()
        self.get_map_based_opp_goal_distance = blackboard.world_model.get_map_based_opp_goal_distance()
        self.get_current_position = blackboard.world_model.get_current_position()
        self.calculate_time_to_ball = blackboard.pathfinding.calculate_time_to_ball()
        self.get_own_goals = blackboard.gamestate.get_own_goals()
        self.get_seconds_remaining = blackboard.gamestate.get_seconds_remaining()
        self.get_red_cards = blackboard.gamestate.get_red_cards()
        self.get_goal_difference = blackboard.gamestate.get_goal_difference()
        self.get_role = blackboard.team_data.get_role()
        self.get_active_teammate_poses = blackboard.team_data.get_active_teammate_poses()
        self.team_rank_to_ball = blackboard.team_data.team_rank_to_ball(self.distance_to_ball)

        # Potentially interesting for future states
        # self.get_ball_goal = blackboard.pathfinding.get_ball_goal(BallGoalType.MAP)
        # self.time_from_pose_to_pose = blackboard.pathfinding.time_from_pose_to_pose()
