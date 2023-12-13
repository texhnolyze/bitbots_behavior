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


class BallSeenNeed(Need):
    def __init__(self, blackboard: BodyBlackboard) -> None:
        self.blackboard: BodyBlackboard = blackboard

    def available(self) -> bool:
        return self.blackboard.world_model.ball_has_been_seen()


class Needs:
    def __init__(self, blackboard: BodyBlackboard) -> None:
        self.blackboard: BodyBlackboard = blackboard
        self.ABLE_TO_MOVE = AbleToMoveNeed(blackboard)
        self.BALL_SEEN = BallSeenNeed(blackboard)
        self.CLOSEST_TO_BALL = ClosestToBallNeed(blackboard)
        self.HAS_BALL = HasBallNeed(blackboard)

    def all(self):
        return [self.ABLE_TO_MOVE, self.BALL_SEEN, self.CLOSEST_TO_BALL, self.HAS_BALL]

    def available(self) -> list[Need]:
        return list(filter(lambda need: need.available(), self.all()))


class ClosestToBallNeed(Need):
    def __init__(self, blackboard: BodyBlackboard) -> None:
        self.blackboard: BodyBlackboard = blackboard
        self.distance_to_ball = self.blackboard.world_model.get_ball_distance()

    def available(self) -> bool:
        return self.blackboard.team_data.team_rank_to_ball(self.distance_to_ball) == 1


class HasBallNeed(Need):
    def __init__(self, blackboard: BodyBlackboard) -> None:
        self.blackboard: BodyBlackboard = blackboard

    def available(self) -> bool:
        return self.blackboard.world_model.get_ball_distance() <= self.blackboard.config.get("ball_approach_dist", 0.0)
