import math

from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class PositioningAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, state: State, new_state: State) -> float:
        total = 0
        highest = 0
        for x in range(1, 3001):
            result = math.sin(x / 1000) ** (x / 1000)
            total += result
            highest = max(result, highest)

        return total / highest

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return [state]
