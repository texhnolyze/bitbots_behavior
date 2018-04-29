# -*- coding:utf-8 -*-
"""
RoleDecider
^^^^^^^^^^^

.. moduleauthor:: Martin Poppinga <1popping@informatik.uni-hamburg.de>

Decides on witch position our fieldie should play
"""
from bitbots_body_behaviour.body.decisions.common.ball_seen import BallSeenFieldie
from bitbots_body_behaviour.body.decisions.team_player.center_decision import CenterDecision
from bitbots_body_behaviour.body.decisions.team_player.defender_decision import DefenderDecision
from bitbots_body_behaviour.body.decisions.team_player.supporter_decision import SupporterDecision
from bitbots_stackmachine.abstract_decision_module import AbstractDecisionModule
from humanoid_league_team_communication.mitecom.mitecom import ROLE_STRIKER, ROLE_SUPPORTER, ROLE_OTHER, ROLE_DEFENDER


class RoleDecider(AbstractDecisionModule):
    def __init__(self, connector, args):
        super(RoleDecider, self).__init__(connector)
        self.forced = args[0] if args else None

    def perform(self, connector, reevaluate=False):
        if self.forced:
            if self.forced == "Striker":
                connector.team_data.set_role(ROLE_STRIKER)
                return self.push(BallSeenFieldie)

            elif self.forced == "Supporter":
                connector.team_data.set_role(ROLE_SUPPORTER)
                return self.push(SupporterDecision)

            elif self.forced == "Center":
                connector.team_data.set_role(ROLE_OTHER)
                return self.push(CenterDecision)

            elif self.forced == "Defender":
                connector.team_data.set_role(ROLE_DEFENDER)
                return self.push(DefenderDecision)
            else:
                raise NotImplementedError
        else:
            # decide by our own
            # if status_ok() # test if robot is capable
            # Todo richtig machen bitte (Martin 7.11.14)
            return self.push(BallSeenFieldie)
            rank_to_ball = connector.team_data_capsule().team_rank_to_ball()
            # print "I'm number ", rank_to_ball
            if rank_to_ball == 1:
                # striker
                connector.team_data_capsule().set_role(ROLE_STRIKER)
                return self.push(BallSeenFieldie)
            elif rank_to_ball in [2, 3, 4]:
                # Supporter
                connector.team_data_capsule().set_role(ROLE_SUPPORTER)
                return self.push(SupporterDecision)
            elif rank_to_ball in [5, 6]:
                # Supporter
                connector.team_data_capsule().set_role(ROLE_OTHER)
                return self.push(CenterDecision)
            else:
                # defender... naja er sollte schon noch hinten stehen
                connector.team_data_capsule().set_role(ROLE_DEFENDER)
                return self.push(DefenderDecision)

    def get_reevaluate(self):
        return True
