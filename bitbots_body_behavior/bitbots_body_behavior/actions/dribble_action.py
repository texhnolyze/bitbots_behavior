from typing import Optional

import numpy as np
from bitbots_msgs.msg import HeadMode
from geometry_msgs.msg import Twist
from rclpy.node import Node

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class DribbleAction(Action):
    def __init__(self, needs: Needs, node: Node):
        super().__init__(needs, node)
        self.needs: list[Need] = [needs.ABLE_TO_MOVE, needs.BALL_SEEN, needs.HAS_BALL]

    def evaluate(self, state: State) -> float:
        return 1.0

    def execute(self, blackboard: BodyBlackboard, _: Optional[State]):
        max_speed_x = blackboard.config["dribble_max_speed_x"]
        max_speed_y = blackboard.config["dribble_max_speed_y"]
        ball_heading_x_vel_zero_point = blackboard.config["dribble_ball_heading_x_vel_zero_point"]
        p = blackboard.config["dribble_p"]
        max_accel_x = blackboard.config["dribble_accel_x"]
        max_accel_y = blackboard.config["dribble_accel_y"]

        blackboard.misc.set_head_mode(HeadMode.LOOK_FRONT)

        current_speed_x = blackboard.pathfinding.current_cmd_vel.linear.x
        current_speed_y = blackboard.pathfinding.current_cmd_vel.linear.y

        ball_v = blackboard.world_model.get_ball_position_uv()
        # Get the relative angle from us to the ball
        ball_angle = blackboard.world_model.get_ball_angle()

        # todo compute yaw speed based on how we are aligned to the goal

        adaptive_acceleration_x = 1 - (abs(ball_angle) / ball_heading_x_vel_zero_point)
        max_speed_x * adaptive_acceleration_x

        current_speed_x = max_accel_x * max_speed_x + current_speed_x * (1 - max_accel_x)

        # give more speed in y direction based on ball position
        y_speed = ball_v[1] * p

        current_speed_y = max_accel_y * np.clip(y_speed, -max_speed_y, max_speed_y) + current_speed_y * (
            1 - max_accel_y
        )

        cmd_vel = Twist()
        cmd_vel.linear.x = current_speed_x
        cmd_vel.linear.y = current_speed_y
        cmd_vel.angular.z = 0.0
        blackboard.pathfinding.direct_cmd_vel_pub.publish(cmd_vel)
