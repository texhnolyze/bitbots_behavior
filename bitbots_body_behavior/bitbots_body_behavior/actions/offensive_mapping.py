from bitbots_body_behavior.state.state import State

class OffensiveMapping():
    def __init__(self) -> None:
        pass

    @staticmethod
    def apply(self, role: [int,float]) -> float:
        #Schaut man auf get_role im blackboard, werden diese als Tuple gespeichert, 
        #wobei der int für die entsprechende Rolle steht
        if (role[0] == 3):
            return 0.8
        elif (role[0] == 5):
            return 0.3
        elif (role[0] == 6):
            return 0.1
        else:
            return 0.0
