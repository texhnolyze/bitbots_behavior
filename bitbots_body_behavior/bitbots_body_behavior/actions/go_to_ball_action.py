from bitbots_blackboard.capsules.pathfinding_capsule import BallGoalType
from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.functions.combinators import AndCombinator, NaturalLogarithm, OrCombinator, Prioritization
from bitbots_body_behavior.functions.utility_functions import (
    EulerExponentialUF,
    ExponentialUF,
    LinearUF,
    NormVerteilungUF,
    PiecewiseUF,
)
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Vector3
from rclpy.duration import Duration

from .action import Action


class GoToBallAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, state: State) -> float:
        # # Block1 der Rolle und allgemeinen Ballposition
        # offensive_mapping = PiecewiseUF.setup(LinearUF.setup(0, 0), 0.5, 0.5)
        # ball_position = ExponentialUF.setup(1, 1, 1)
        # combinator_eins = NaturalLogarithm.apply([offensive_mapping, ball_position], 5)

        # # Block2 Winkel und Distanz
        # ball_angle = NormVerteilungUF.setup(0.25)
        # ball_distance = EulerExponentialUF.setup(1, -1, 1)
        # combinator_zwei = AndCombinator.apply(
        #     [ball_angle.apply(self, state.angle_to_ball), ball_distance.apply(self, state.distance_to_ball)]
        # )

        # combinator_b1_b2 = Prioritization.apply([combinator_eins, combinator_zwei], [2, 8])

        # # Block3 Spielsituation
        # goal_difference = PiecewiseUF.setup(LinearUF.setup(-1, 8, 0.5), 4, -4)
        # seconds_remaining = PiecewiseUF.setup(LinearUF.setup(-1, 30, 1), 30, 0)
        # combinator_drei = Prioritization.apply([goal_difference, seconds_remaining], [9, 1])

        # return OrCombinator.apply([combinator_b1_b2, combinator_drei])

        return 1

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return []
    
    def execute(self, blackboard: BodyBlackboard, _):
        pose_msg = blackboard.pathfinding.get_ball_goal(BallGoalType.MAP , 0)
        blackboard.pathfinding.publish(pose_msg)

        approach_marker = Marker()
        approach_marker.pose.position.x = 0
        approach_marker.type = Marker.SPHERE
        approach_marker.action = Marker.MODIFY
        approach_marker.id = 1
        color = ColorRGBA()
        color.r = 1.0
        color.g = 1.0
        color.b = 1.0
        color.a = 1.0
        approach_marker.color = color
        approach_marker.lifetime = Duration(seconds=0.5).to_msg()
        scale = Vector3(x=0.2, y=0.2, z=0.2)
        approach_marker.scale = scale
        approach_marker.header.stamp = blackboard.node.get_clock().now().to_msg()
        approach_marker.header.frame_id = blackboard.world_model.base_footprint_frame

        blackboard.pathfinding.approach_marker_pub.publish(approach_marker)

    

