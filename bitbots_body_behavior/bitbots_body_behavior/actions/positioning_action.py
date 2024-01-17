import math
from typing import Tuple

import numpy as np
from bitbots_msgs.msg import HeadMode
from bitbots_utils.transforms import quat_from_yaw
from geometry_msgs.msg import PoseStamped

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.considerations.defensiveness import Defensiveness
from bitbots_body_behavior.considerations.offensiveness import Offensiveness
from bitbots_body_behavior.functions.combinators import (
    OrCombinator,
)
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action

Point = Tuple[float, float, float]


class PositioningAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, _: State, new_state: State) -> float:
        offensiveness = Offensiveness.get_utility_value(new_state)
        defensiveness = Defensiveness.get_utility_value(new_state)

        return OrCombinator.apply([offensiveness, defensiveness])

    def next_states_to_evaluate(self, state: State) -> list[State]:
        # generate the next possible positions in a circle around the current position
        # with an offset of 0.5m in each direction 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°
        walk_distance = 0.5
        potential_future_positions = np.array(self.generate_potential_positions(state.current_position, walk_distance))
        teammate_positions = np.array(state.active_teammate_poses)

        if len(teammate_positions) > 0:
            # calculate the distance to each teammate resulting in a matrix
            # where each column is a teammate and each row is a potential future position
            distances_to_teammates = np.linalg.norm(
                potential_future_positions[:, np.newaxis, :2] - teammate_positions[np.newaxis, :, :2], axis=2
            )
            # by take the minimum of each row we get the distance to the closest teammate
            # for each potential future position
            distance_to_next_teammate = np.min(distances_to_teammates, axis=1)

            next_positions = potential_future_positions[distance_to_next_teammate > walk_distance]
        else:
            next_positions = potential_future_positions

        return list(map(state.set_current_position, next_positions))

    def generate_potential_positions(self, current_position: Point, distance: float = 1.0) -> list[Point]:
        points = [current_position]
        x, y, theta = current_position

        # setup up the angles for the 8 points around the current position based on the unit circle
        angles = [0, math.pi / 4, math.pi / 2, 3 * math.pi / 4, math.pi, -3 * math.pi / 4, -math.pi / 2, -math.pi / 4]

        for angle in angles:
            new_x = x + distance * math.cos(theta + angle)
            new_y = y + distance * math.sin(theta + angle)
            new_theta = theta + angle

            points.append((new_x, new_y, new_theta))

        return points

    def execute(self, blackboard: BodyBlackboard, new_state: State):
        blackboard.misc.set_head_mode(HeadMode.BALL_MODE)

        pose_msg = PoseStamped()
        pose_msg.header.stamp = blackboard.node.get_clock().now().to_msg()
        pose_msg.header.frame_id = blackboard.map_frame

        pose_msg.pose.position.x = new_state.current_position[0]
        pose_msg.pose.position.y = new_state.current_position[1]
        pose_msg.pose.position.z = 0.0
        pose_msg.pose.orientation = quat_from_yaw(math.radians(new_state.current_position[2]))
        blackboard.pathfinding.publish(pose_msg)
