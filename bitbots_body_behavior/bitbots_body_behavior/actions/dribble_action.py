from random import random

from bitbots_body_behavior.state.needs import Need, Needs
from bitbots_body_behavior.state.state import State

from .action import Action


class DribbleAction(Action):
    def __init__(self, needs: Needs):
        self.needs: list[Need] = [needs.ABLE_TO_MOVE]

    def evaluate(self, state: State, new_state: State) -> float:
        return random()

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return [state]
