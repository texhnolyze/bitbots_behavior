import math

from geometry_msgs.msg import PoseStamped
from bitbots_utils.transforms import quat_from_yaw

from bitbots_blackboard.blackboard import BodyBlackboard
from bitbots_body_behavior.functions.combinators import (
    AndCombinator,
    NaturalLogarithm,
    OrCombinator,
    Prioritization,
    Inverter,
)
from bitbots_body_behavior.functions.utility_functions import (
    EulerExponentialUF,
    SigmoidUF,
    ExponentialUF,
    LinearUF,
    NormVerteilungUF,
    PiecewiseUF,
)
from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State
import math
from copy import deepcopy
from bitbots_body_behavior.actions.offensive_mapping import OffensiveMapping


from .action import Action


class PositioningAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, state: State, new_state: State) -> float:
        #Offensive Mapping
        offensive_mapping = OffensiveMapping.apply(state.role)

        #Block 1: Offensive Positionierung vorm Tor
        opp_goal_x_diff = ExponentialUF.setup(1,1,1).apply(state.map_based_opp_goal_center_xy[0] - new_state.current_position[0])
        #Fehlerhaft, Sigmoid muss be 2. Variante kriegen
        opp_goal_y_diff = SigmoidUF.setup(-0.5, 2*math.e).apply(state.map_based_opp_goal_center_xy[1] - new_state.current_position[1])
        offense_positioning = Prioritization.apply([opp_goal_x_diff, opp_goal_y_diff], [3, 7])

        combinator_offmap_off = NaturalLogarithm.apply([offense_positioning, offensive_mapping], 5)

        #Block 2: Defensive Positionierung vorm Ball (vielleicht auch zwischen Ball und own_goal möglich?)
        ball_x_diff = ExponentialUF.setup(1,1,1).apply(state.ball_position_xy[0] - new_state.current_position[0])
        ball_y_diff = ExponentialUF.setup(1,1,1).apply(state.ball_position_xy[1] - new_state.current_position[1])
        defense_positioning = AndCombinator.apply([ball_x_diff, ball_y_diff])

        combinator_offmap_def = NaturalLogarithm.apply([offensive_mapping, Inverter.apply(defense_positioning)], 5)

        allg_positioning = OrCombinator.apply([combinator_offmap_off, combinator_offmap_def])

        #Spielsituation
        new_x_position = ExponentialUF.setup(1,1,1).apply(new_state.current_position[0])

        # Block 3: Spielsituation
        goal_difference = PiecewiseUF.setup(LinearUF.setup(-1, 8, 0.5), 4, -4).apply(state.goal_difference)
        seconds_remaining = PiecewiseUF.setup(LinearUF.setup(-1, 30, 1), 30, 0).apply(state.seconds_remaining)

        game_pressure = Prioritization.apply([goal_difference, seconds_remaining], [9, 1])

        pressing = NaturalLogarithm.apply([new_x_position, game_pressure], 5)

        #Angle und Distance zur new_position berechnen und einbinden?

        return OrCombinator.apply(allg_positioning, pressing)

    def next_states_to_evaluate(self, state: State) -> list[State]:
        current_state = state.current_position
        teammate_states = state.active_teammate_poses
        new_states = []
        future_positions = list([current_state[0] +0.5 , current_state[1], current_state[2]], 
                    [current_state[0], current_state[1] + 0.5, current_state[2]], 
                    [current_state[0] + math.sqrt(0.5) , current_state[1] + math.sqrt(0.5), current_state[2]],
                    [current_state[0] -0.5 , current_state[1], current_state[2]], 
                    [current_state[0], current_state[1] -0.5, current_state[2]], 
                    [current_state[0] - math.sqrt(0.5), current_state[1] - math.sqrt(0.5), current_state[2]],
                    [current_state[0] + math.sqrt(0.5), current_state[1] - math.sqrt(0.5), current_state[2]],
                    [current_state[0] - math.sqrt(0.5), current_state[1] + math.sqrt(0.5), current_state[2]])
        
        for position in future_positions:
            for state in teammate_states:
                if position == state:
                    future_positions.remove(position)

        for i in range(len(future_positions)):
            new_state = State()
            #new_state.deepcopy()
            new_state.current_position = future_positions[i]

            new_states.append(new_state)

        return new_states
    
    def execute(self, blackboard: BodyBlackboard, new_state: State):
        pose_msg = PoseStamped()
        pose_msg.header.stamp = blackboard.node.get_clock().now().to_msg()
        pose_msg.header.frame_id = blackboard.map_frame

        pose_msg.pose.position.x = new_state.current_position[0]
        pose_msg.pose.position.y = new_state.current_position[0]
        pose_msg.pose.position.z = 0
        pose_msg.pose.orientation = quat_from_yaw(math.radians(self.point[2]))

        blackboard.pathfinding.publish(pose_msg)
        return super().execute(blackboard, new_state)
