from bitbots_msgs.msg import GameState

from bitbots_blackboard.blackboard import BodyBlackboard


class Need:
    def available(self) -> bool:
        raise NotImplementedError


class AbleToMoveNeed(Need):
    def __init__(self, blackboard: BodyBlackboard) -> None:
        self.blackboard: BodyBlackboard = blackboard

    def available(self) -> bool:
        gamestate = self.blackboard.gamestate.get_gamestate()
        game_is_running = gamestate in [
            GameState.GAMESTATE_READY,
            GameState.GAMESTATE_PLAYING,
        ]
        return (
            game_is_running
            and not self.blackboard.gamestate.get_is_penalized()
            and not self.blackboard.kick.is_currently_kicking
        )


class Needs:
    def __init__(self, blackboard: BodyBlackboard) -> None:
        self.blackboard: BodyBlackboard = blackboard
        self.ABLE_TO_MOVE = AbleToMoveNeed(blackboard)

    def all(self):
        return [self.ABLE_TO_MOVE]

    def available(self) -> list[Need]:
        return list(filter(lambda need: need.available(), self.all()))
