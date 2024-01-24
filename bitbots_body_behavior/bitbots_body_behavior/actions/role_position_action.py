from bitbots_msgs.msg import HeadMode
from tf2_geometry_msgs import PoseStamped

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class RolePositionAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.READY_STATE]
        self.ready_state = needs.READY_STATE.available

    def evaluate(self, state: State) -> float:
        if self.ready_state:
            return 1.0
        else:
            return 0.0

    def role_positions(self, blackboard: BodyBlackboard):
        role_positions = blackboard.config["role_positions"]
        kickoff_type = "active" if blackboard.gamestate.has_kickoff() else "passive"
        try:
            if blackboard.team_data.role == "goalie":
                generalized_role_position = role_positions[blackboard.team_data.role]
            else:
                # players other than the goalie have multiple possible positions
                generalized_role_position = role_positions[blackboard.team_data.role][kickoff_type][
                    str(blackboard.misc.position_number)
                ]
        except KeyError as e:
            raise KeyError(f"Role position for {blackboard.team_data.role} not specified in config") from e

        # Adapt position to field size
        # TODO know where map frame is located
        role_position = [
            generalized_role_position[0] * blackboard.world_model.field_length / 2,
            generalized_role_position[1] * blackboard.world_model.field_width / 2,
        ]

        return role_position

    def execute(self, blackboard: BodyBlackboard, state: State):
        blackboard.misc.set_head_mode(HeadMode.BALL_MODE)

        pose_msg = PoseStamped()
        pose_msg.header.stamp = blackboard.node.get_clock().now().to_msg()
        pose_msg.header.frame_id = blackboard.map_frame

        role_position = self.role_positions(blackboard)

        pose_msg.pose.position.x = role_position[0]
        pose_msg.pose.position.y = role_position[1]
        pose_msg.pose.orientation.w = 1.0

        blackboard.pathfinding.publish(pose_msg)
