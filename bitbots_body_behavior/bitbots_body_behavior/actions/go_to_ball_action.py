from typing import Optional

from bitbots_msgs.msg import HeadMode
from geometry_msgs.msg import Vector3
from rclpy.duration import Duration
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_blackboard.capsules.pathfinding_capsule import BallGoalType
from bitbots_body_behavior.considerations.ball_closeness import BallCloseness
from bitbots_body_behavior.considerations.game_pressure import GamePressure
from bitbots_body_behavior.considerations.pressing import Pressing
from bitbots_body_behavior.functions.combinators import (
    OrCombinator,
    Prioritization,
)
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class GoToBallAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE, needs.BALL_SEEN, needs.CLOSEST_TO_BALL]

    def evaluate(self, state: State) -> float:
        pressing = Pressing.get_utility_value(state)
        ball_closeness = BallCloseness.get_utility_value(state)
        ball_consideration = Prioritization.apply([pressing, ball_closeness], [2, 8])

        game_pressure = GamePressure.get_utility_value(state)

        return OrCombinator.apply([ball_consideration, game_pressure])

    def execute(self, blackboard: BodyBlackboard, _: Optional[State]):
        pose_distance_from_ball = blackboard.config.get("ball_approach_dist", 0.0)

        if blackboard.world_model.get_ball_distance() > 1.5:
            blackboard.misc.set_head_mode(HeadMode.BALL_MODE)
        else:
            blackboard.misc.set_head_mode(HeadMode.LOOK_FRONT)

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
