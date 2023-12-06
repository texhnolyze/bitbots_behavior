import math
from typing import Tuple

import numpy as np
from bitbots_utils.transforms import quat_from_yaw
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
from bitbots_body_behavior.functions.utility_functions import (
    ExponentialUF,
    LinearUF,
    PiecewiseUF,
    SigmoidUF,
)
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
        opp_goal_x_diff = ExponentialUF.setup(1, 1, 1).apply(
            state.map_based_opp_goal_center_xy[0] - new_state.current_position[0]
        )
        # Fehlerhaft, Sigmoid muss be 2. Variante kriegen
        opp_goal_y_diff = SigmoidUF.setup(-0.5, 2 * math.e).apply(
            state.map_based_opp_goal_center_xy[1] - new_state.current_position[1]
        )
        offense_positioning = Prioritization.apply([opp_goal_x_diff, opp_goal_y_diff], [3, 7])

        combinator_offmap_off = NaturalLogarithm.apply([offense_positioning, offensive_mapping], 5)

        # Block 2: Defensive Positionierung vorm Ball (vielleicht auch zwischen Ball und own_goal möglich?)
        ball_x_diff = ExponentialUF.setup(1, 1, 1).apply(state.ball_position_xy[0] - new_state.current_position[0])
        ball_y_diff = ExponentialUF.setup(1, 1, 1).apply(state.ball_position_xy[1] - new_state.current_position[1])
        defense_positioning = AndCombinator.apply([ball_x_diff, ball_y_diff])

        combinator_offmap_def = NaturalLogarithm.apply([offensive_mapping, Inverter.apply(defense_positioning)], 5)

        allg_positioning = OrCombinator.apply([combinator_offmap_off, combinator_offmap_def])

        # Spielsituation
        new_x_position = ExponentialUF.setup(1, 1, 1).apply(new_state.current_position[0])

        # Block 3: Spielsituation
        goal_difference = PiecewiseUF.setup(LinearUF.setup(-1, 8, 0.5), 4, -4).apply(state.goal_difference)
        seconds_remaining = PiecewiseUF.setup(LinearUF.setup(-1, 30, 1), 30, 0).apply(state.seconds_remaining)

        game_pressure = Prioritization.apply([goal_difference, seconds_remaining], [9, 1])

        pressing = NaturalLogarithm.apply([new_x_position, game_pressure], 5)

        # Angle und Distance zur new_position berechnen und einbinden?
        return OrCombinator.apply(allg_positioning, pressing)

    def next_states_to_evaluate(self, state: State) -> list[State]:
        # generate the next possible positions in a circle around the current position
        # with an offset of 0.5m in each direction 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°
        walk_distance = 0.5
        potential_future_positions = self.generate_potential_positions(state.current_position, walk_distance)
        next_positions = np.empty((0, 3))

        for own_position in potential_future_positions:
            in_walking_distance = False

            for teammate_position in state.active_teammate_poses:
                distance_to_teammate = np.linalg.norm(np.array(own_position) - np.array(teammate_position))

                if distance_to_teammate < walk_distance:
                    in_walking_distance = True
                    break

            if not in_walking_distance:
                next_positions = np.vstack((next_positions, own_position))

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

    # def generate_potential_positions(self, current_position: Point, distance: float = 0.5) -> list[Point]:
    #     points = [current_position]
    #     x, y, theta = current_position

    #     offsets = [
    #         (distance, 0),  # Right
    #         (distance * math.sqrt(0.5), -distance * math.sqrt(0.5)),  # Back-Right
    #         (0, -distance),  # Back
    #         (-distance * math.sqrt(0.5), -distance * math.sqrt(0.5)),  # Back-Left
    #         (-distance, 0),  # Left
    #         (-distance * math.sqrt(0.5), distance * math.sqrt(0.5)),  # Front-Left
    #         (0, distance),  # Front
    #         (distance * math.sqrt(0.5), distance * math.sqrt(0.5)),  # Front-Right
    #     ]

    #     for offset_x, offset_y in offsets:
    #         new_x = x + offset_x
    #         new_y = y + offset_y
    #         # new_x = x + offset_x * math.cos(theta) - offset_y * math.sin(theta)
    #         # new_y = y + offset_x * math.sin(theta) + offset_y * math.cos(theta)

    #         points.append((new_x, new_y, theta))

    #     return points

    def execute(self, blackboard: BodyBlackboard, new_state: State):
        pose_msg = PoseStamped()
        pose_msg.header.stamp = blackboard.node.get_clock().now().to_msg()
        pose_msg.header.frame_id = blackboard.map_frame

        pose_msg.pose.position.x = new_state.current_position[0]
        pose_msg.pose.position.y = new_state.current_position[1]
        pose_msg.pose.position.z = 0
        pose_msg.pose.orientation = quat_from_yaw(math.radians(self.point[2]))

        blackboard.pathfinding.publish(pose_msg)
