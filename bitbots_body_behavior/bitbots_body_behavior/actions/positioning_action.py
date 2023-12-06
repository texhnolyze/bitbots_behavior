from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State
import math
from copy import deepcopy

from .action import Action


class PositioningAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, state: State, new_state: State) -> float:
        return 0

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

