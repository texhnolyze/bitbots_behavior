from typing import Optional

from geometry_msgs.msg import Vector3
from rclpy.duration import Duration
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_blackboard.capsules.pathfinding_capsule import BallGoalType
from bitbots_body_behavior.functions.combinators import (
    AndCombinator,
    NaturalLogarithm,
    OrCombinator,
    Prioritization,
)
from bitbots_body_behavior.functions.utility_functions import (
    EulerExponentialUF,
    ExponentialUF,
    LinearUF,
    NormVerteilungUF,
    PiecewiseUF,
)
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class GoToBallAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE, needs.BALL_SEEN]

    def evaluate(self, state: State) -> float:
        # Block1 der Rolle und allgemeinen Ballposition
        # offensive_mapping = PiecewiseUF.setup(LinearUF.setup(0, 0), 0.5, 0.5)
        offensive_mapping = 0.5
        ball_position_x = ExponentialUF.setup(1, 1, 1).apply(state.ball_position_xy[0])
        pressing = NaturalLogarithm.apply([offensive_mapping, ball_position_x], 5)

        # Block2 Winkel und Distanz
        ball_angle = NormVerteilungUF.setup(0.25).apply(state.angle_to_ball)
        ball_distance = EulerExponentialUF.setup(1, -1, 1).apply(state.distance_to_ball)
        ball_closeness = AndCombinator.apply([ball_angle, ball_distance])

        combinator_b1_b2 = Prioritization.apply([pressing, ball_closeness], [2, 8])

        # Block3 Spielsituation
        goal_difference = PiecewiseUF.setup(LinearUF.setup(-1, 8, 0.5), 4, -4).apply(state.goal_difference)
        seconds_remaining = PiecewiseUF.setup(LinearUF.setup(-1, 30, 1), 30, 0).apply(state.seconds_remaining)

        game_pressure = Prioritization.apply([goal_difference, seconds_remaining], [9, 1])

        return OrCombinator.apply([combinator_b1_b2, game_pressure])

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return []

    def execute(self, blackboard: BodyBlackboard, _: Optional[State]):
        pose_distance_from_ball = 0.0
        pose_msg = blackboard.pathfinding.get_ball_goal(BallGoalType.MAP, pose_distance_from_ball)
        blackboard.pathfinding.publish(pose_msg)

        approach_marker = Marker()
        approach_marker.pose.position.x = pose_distance_from_ball
        approach_marker.type = Marker.SPHERE
        approach_marker.action = Marker.MODIFY
        approach_marker.id = 1
        approach_marker.color = ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0)
        approach_marker.lifetime = Duration(seconds=0.5).to_msg()
        approach_marker.scale = Vector3(x=0.2, y=0.2, z=0.2)
        approach_marker.header.stamp = blackboard.node.get_clock().now().to_msg()
        approach_marker.header.frame_id = blackboard.world_model.base_footprint_frame

        blackboard.pathfinding.approach_marker_pub.publish(approach_marker)
