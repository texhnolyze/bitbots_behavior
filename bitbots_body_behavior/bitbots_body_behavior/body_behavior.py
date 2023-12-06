#!/usr/bin/env python3

import rclpy
import tf2_ros as tf2
from bitbots_msgs.msg import GameState, RobotControlState, TeamData
from bitbots_tf_listener import TransformListener
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist, TwistWithCovarianceStamped
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.duration import Duration
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from soccer_vision_3d_msgs.msg import RobotArray

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.evaluation import SyncEvaluator
from bitbots_body_behavior.state.needs import Needs
from bitbots_body_behavior.state.state import State

from .action_decider import ActionDecider


class BodyBehavior:
    def __init__(self, node: Node):
        self.counter = 0
        self.step_running = False
        self.node = node

        self.tf_buffer = tf2.Buffer(cache_time=Duration(seconds=30))
        self.tf_listener = TransformListener(self.tf_buffer, node)

        self.blackboard = BodyBlackboard(node, self.tf_buffer)

        self.setup_action_decider()
        self.setup_subscriptions()

    def setup_action_decider(self):
        state = State(self.blackboard)
        needs = Needs(self.blackboard)
        self.decider = ActionDecider(self.blackboard, state, needs, SyncEvaluator(), self.node.get_logger())

    # def setup_dsd(self):
    #     self.dsd = DSD(
    #         self.blackboard, "debug/dsd/body_behavior", self.node
    #     )  # TODO: use config

    #     dirname = get_package_share_directory("bitbots_body_behavior")
    #     self.dsd.register_actions(os.path.join(dirname, "dsd_actions"))
    #     self.dsd.register_decisions(os.path.join(dirname, "dsd_decisions"))
    #     dsd_file = (
    #         self.node.get_parameter("dsd_file").get_parameter_value().string_value
    #     )
    #     self.dsd.load_behavior(os.path.join(dirname, dsd_file))

    def setup_subscriptions(self):
        self.node.create_subscription(
            PoseWithCovarianceStamped,
            "ball_position_relative_filtered",
            self.blackboard.world_model.ball_filtered_callback,
            qos_profile=1,
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        self.node.create_subscription(
            GameState,
            "gamestate",
            self.blackboard.gamestate.gamestate_callback,
            qos_profile=1,
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        self.node.create_subscription(
            TeamData,
            "team_data",
            self.blackboard.team_data.team_data_callback,
            qos_profile=1,
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        self.node.create_subscription(
            PoseWithCovarianceStamped,
            "pose_with_covariance",
            self.blackboard.world_model.pose_callback,
            qos_profile=1,
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        self.node.create_subscription(
            RobotArray,
            "robots_relative_filtered",
            self.blackboard.costmap.robot_callback,
            qos_profile=1,
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        self.node.create_subscription(
            RobotControlState,
            "robot_state",
            self.blackboard.misc.robot_state_callback,
            qos_profile=1,
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        self.node.create_subscription(
            TwistWithCovarianceStamped,
            self.node.get_parameter("body.ball_movement_subscribe_topic").get_parameter_value().string_value,
            self.blackboard.world_model.ball_twist_callback,
            qos_profile=1,
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        self.node.create_subscription(
            Twist,
            "cmd_vel",
            self.blackboard.pathfinding.cmd_vel_cb,
            qos_profile=1,
            callback_group=MutuallyExclusiveCallbackGroup(),
        )

    def run(self):
        try:
            self.decider.decide()
            self.decider.execute_ideal_action()

            self.blackboard.team_data.publish_strategy()
            self.blackboard.team_data.publish_time_to_ball()
            self.counter = (self.counter + 1) % self.blackboard.config["time_to_ball_divider"]
            if self.counter == 0:
                self.blackboard.pathfinding.calculate_time_to_ball()
        except Exception as e:
            import traceback

            traceback.print_exc()
            self.node.get_logger().error(str(e))


def main(args=None):
    rclpy.init(args=None)
    node = Node("body_behavior", automatically_declare_parameters_from_overrides=True)
    body_behavior = BodyBehavior(node)
    node.create_timer(
        1 / 60.0,
        body_behavior.run,
        callback_group=MutuallyExclusiveCallbackGroup(),
        clock=node.get_clock(),
    )

    # Number of executor threads is the number of MutiallyExclusiveCallbackGroups + 2 threads needed by the tf listener and executor
    multi_executor = MultiThreadedExecutor(num_threads=12)
    multi_executor.add_node(node)

    try:
        multi_executor.spin()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
