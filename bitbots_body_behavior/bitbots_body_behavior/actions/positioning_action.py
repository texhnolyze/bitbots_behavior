import math
from typing import Tuple

import numpy as np
from geometry_msgs.msg import PoseStamped

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.considerations.offensive_mapping import OffensiveMapping
from bitbots_body_behavior.functions.combinators import (
    AndCombinator,
    Inverter,
    NaturalLogarithm,
    OrCombinator,
    Prioritization,
)
from bitbots_body_behavior.functions.utility_functions import SigmoidTwoXUF
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action

Point = Tuple[float, float, float]


class PositioningAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, state: State, new_state: State) -> float:
        # Offensive Mapping
        offensive_mapping = OffensiveMapping.apply(state.role)

        # Block 1: Offensive Positionierung vorm Tor
        opp_goal_x_diff = SigmoidTwoXUF.setup(1, 1.65, -1, 0.7).apply(
            state.map_based_opp_goal_center_xy[0] - new_state.current_position[0]
        )
        if opp_goal_x_diff > 1:
            opp_goal_x_diff = 1
        # Fehlerhaft, Sigmoid muss be 2. Variante kriegen
        opp_goal_y_diff = SigmoidTwoXUF.setup(-0.5, 2).apply(
            state.map_based_opp_goal_center_xy[1] - new_state.current_position[1]
        )
        offense_positioning = Prioritization.apply([opp_goal_x_diff, opp_goal_y_diff], [3, 7])

        combinator_offmap_off = NaturalLogarithm.apply([offense_positioning, offensive_mapping], 5)

        # Block 2: Defensive Positionierung vorm Ball (vielleicht auch zwischen Ball und own_goal möglich?)
        ball_x_diff = SigmoidTwoXUF.setup(1, 1.65, -1, 0.7).apply(
            state.ball_position_xy[0] - new_state.current_position[0]
        )
        if ball_x_diff > 1:
            ball_x_diff = 1
        ball_y_diff = SigmoidTwoXUF.setup(-0.5, 2).apply(state.ball_position_xy[1] - new_state.current_position[1])
        defense_positioning = AndCombinator.apply([ball_x_diff, ball_y_diff])

        combinator_offmap_def = NaturalLogarithm.apply([offensive_mapping, Inverter.apply(defense_positioning)], 5)

        return OrCombinator.apply([combinator_offmap_off, combinator_offmap_def])

    def next_states_to_evaluate(self, state: State) -> list[State]:
        # generate the next possible positions in a circle around the current position
        # with an offset of 0.5m in each direction 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°
        walk_distance = 0.5
        potential_future_positions = np.array(self.generate_potential_positions(state.current_position, walk_distance))
        teammate_positions = np.array(state.active_teammate_poses)

        if len(teammate_positions) > 0:
            distances_to_teammates = np.linalg.norm(
                potential_future_positions - teammate_positions[:, np.newaxis, :], axis=2
            )
            distance_to_next_teammate = np.min(distances_to_teammates, axis=0)

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

            points.append((new_x, new_y, theta))

        return points

    def execute(self, blackboard: BodyBlackboard, new_state: State):
        pose_msg = PoseStamped()
        pose_msg.header.stamp = blackboard.node.get_clock().now().to_msg()
        pose_msg.header.frame_id = blackboard.map_frame

        pose_msg.pose.position.x = new_state.current_position[0]
        pose_msg.pose.position.y = new_state.current_position[1]
        pose_msg.pose.position.z = 0.0
        # pose_msg.pose.orientation = quat_from_yaw(math.radians(self.point[2]))

        blackboard.pathfinding.publish(pose_msg)
