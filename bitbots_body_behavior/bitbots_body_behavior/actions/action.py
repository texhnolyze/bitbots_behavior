from bitbots_body_behavior.state.needs import Needs
from bitbots_body_behavior.state.state import State


class Action:
    def __init__(self, needs: Needs):
        self.needs: list[Needs] = []

    def execute(self, new_state: State):
        raise NotImplementedError

    def evaluate(self, state: State, new_state: State) -> float:
        raise NotImplementedError

    def next_states_to_evaluate(self, state: State) -> list[State]:
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__
