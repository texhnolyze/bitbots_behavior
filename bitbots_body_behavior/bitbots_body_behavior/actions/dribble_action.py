from typing import Optional

import numpy as np

from geometry_msgs.msg import Twist
from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.considerations.offensive_mapping import OffensiveMapping
from bitbots_body_behavior.functions.combinators import (
    Prioritization,
)
from bitbots_body_behavior.functions.utility_functions import (
    LinearUF,
    PiecewiseUF,
)
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class DribbleAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE, needs.HAS_BALL]
       
        

    def evaluate(self, state: State) -> float:
        return 1.0

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return []
    
    def execute(self, blackboard: BodyBlackboard, new_state: State | None):
        max_speed_x = blackboard.config["dribble_max_speed_x"]
        min_speed_x = -0.1
        max_speed_y = blackboard.config["dribble_max_speed_y"]
        ball_heading_x_vel_zero_point = blackboard.config["dribble_ball_heading_x_vel_zero_point"]
        p = blackboard.config["dribble_p"]
        max_accel_x = blackboard.config["dribble_accel_x"]
        max_accel_y = blackboard.config["dribble_accel_y"]

        current_speed_x = blackboard.pathfinding.current_cmd_vel.linear.x
        current_speed_y = blackboard.pathfinding.current_cmd_vel.linear.y
       
        ball_v = blackboard.world_model.get_ball_position_uv()
        # Get the relative angle from us to the ball
        ball_angle = blackboard.world_model.get_ball_angle()

        # todo compute yaw speed based on how we are aligned to the goal

        adaptive_acceleration_x = 1 - (abs(ball_angle) / ball_heading_x_vel_zero_point)
        max_speed_x * adaptive_acceleration_x

        current_speed_x = max_accel_x *max_speed_x + current_speed_x * (1 -max_accel_x)

        # give more speed in y direction based on ball position
        y_speed = ball_v * p

        current_speed_y = max_accel_y * np.clip(
            y_speed, -max_speed_y,max_speed_y
        ) + current_speed_y * (1 - max_accel_y)

        cmd_vel = Twist()
        cmd_vel.linear.x = current_speed_x
        cmd_vel.linear.y = current_speed_y
        cmd_vel.angular.z = 0.0
        blackboard.pathfinding.direct_cmd_vel_pub.publish(cmd_vel)

