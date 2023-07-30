from .elevators import Elevator


class ElevatorsSystem:
    """ this method is using for initialising Elevator System for all elevator and also creating elevator object

     """
    def __init__(self, elevatorsDetailsInMap):
        self.elevators = []
        self.elevatorsDetailsInMap = elevatorsDetailsInMap
        for each in self.elevatorsDetailsInMap:
            direction = self.elevatorsDetailsInMap[each][0]  # direction
            serviceList = self.elevatorsDetailsInMap[each][2]  # serviceList
            currentPositionOfElevator = self.elevatorsDetailsInMap[each][1]  # current floor
            new_elevator = Elevator(each, -4, 12, currentPositionOfElevator, serviceList, direction)
            # 12 is max floor and -4 min floor
            self.elevators.append(new_elevator)  # creating elevator object

