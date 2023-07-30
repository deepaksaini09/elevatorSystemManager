import datetime

from django.db import connection


class Elevator:
    """
    for a single elevator request processing
    """

    def __init__(self, lift_number, min_floor, max_floor, lift_positions, serviceList, directionOfLift):
        self.lift_number = lift_number
        self.is_operational = True
        self.floor_max = min_floor
        self.floor_min = max_floor
        self.on_floor = lift_positions
        self.direction = directionOfLift
        self.openAndClose = False
        self.currentStatus = lift_positions
        self.service_list = serviceList

    def doorOpen(self):
        """ for door open and also updating into table its status like
           1 or True - open door
        """
        print(f'lift {self.lift_number} door is open')
        self.openAndClose = True
        SQL = """ 
                update elevator_elevator
                set is_door_close_open =%s
                where lift_number = %s;
         """
        cursor = connection.cursor()
        cursor.execute(SQL, (True, self.lift_number))
        connection.commit()
        connection.close()

    def closeDoor(self):
        """ for door close and also updating into table its status like
           0 or False - close door
        """
        self.openAndClose = False
        print(f'lift {self.lift_number} door is close')
        SQL = """ 
                        update elevator_elevator
                        set is_door_close_open =%s
                        where lift_number = %s;
                 """
        cursor = connection.cursor()
        cursor.execute(SQL, (False, self.lift_number))
        connection.commit()
        connection.close()

    def currentFloorStatus(self):
        """ for updating current floor status of elevator
            like
            0- floor number is 0
             1- floor number is 1
             .......
        """
        print(f'lift {self.lift_number} current floor {self.on_floor}')
        SQL = """ 
                        update elevator_elevator
                        set current_floor =%s
                        where lift_number = %s;
                 """
        cursor = connection.cursor()
        cursor.execute(SQL, (self.on_floor, self.lift_number))
        connection.commit()
        connection.close()

    def elevatorServiceDirection(self, direction=None):
        """ for updating direction of elevator
           0 - for rest
           1- going up
           -1 - going down
        """
        print(f"lift {self.lift_number} current direction", 'above going' if self.direction == 1 else 'below going')
        SQL = """ 
                                update elevator_elevator
                                set moving_up =%s
                                where lift_number = %s;
                         """
        if direction:
            self.direction = 0
        cursor = connection.cursor()
        cursor.execute(SQL, (self.direction, self.lift_number))
        connection.commit()
        connection.close()

    def assignRequest(self, assignRequest):
        """ this method is used to take user request for appropriate elevator
            and append data for its service list and process floor request one by one
        """
        self.service_list.append(assignRequest)

    def commonFunForRequestProcess(self, userRequest):
        """ this is common method for
            - checking floor number request is exist in its service list(exist multiple floor number )
            - when elevator reaches for particular floor then it will remove from its service list
            and also in tables(elevator_floorrequest) it is archived
        """
        try:
            if self.service_list.count(userRequest):
                self.service_list.remove(userRequest)
                self.doorOpen()
                self.closeDoor()
                self.currentFloorStatus()
                self.elevatorServiceDirection()
        except Exception as error:
            print(error)

    def processRequest(self):
        """
          in this method here we are processing one elevator request for its service list with the help of
          direction like 0(rest), 1(going up), -1(going down) and also calling method of close door,
          open door, updating elevator direction and also updating its status into database
        """
        if self.direction == 0:
            self.direction = 1
            if self.service_list[0] < self.on_floor:
                self.direction = -1
        if self.direction:
            print(self.service_list)
            while self.service_list:
                currentFloor = self.on_floor
                if self.direction == 1:
                    for userRequest in range(self.on_floor, max(self.service_list) + 1):
                        self.on_floor = userRequest
                        self.commonFunForRequestProcess(userRequest)
                    self.direction = 0
                    print(self.service_list)
                    if self.service_list:
                        self.direction = -1
                        minFloorServiceRequest = min(self.service_list)
                        for userRequest in range(self.on_floor, minFloorServiceRequest - 1, -1):
                            print(userRequest, self.on_floor)
                            self.on_floor = userRequest
                            self.commonFunForRequestProcess(userRequest)
                            if not self.service_list:
                                break
                    self.direction = 0
                    if not self.service_list:
                        break
                if self.direction == -1:  # for direction going down
                    minFloorServiceRequest = min(self.service_list)
                    print(minFloorServiceRequest, self.on_floor)
                    for userRequest in range(self.on_floor, minFloorServiceRequest - 1, -1):
                        self.on_floor = userRequest
                        self.commonFunForRequestProcess(userRequest)
                    self.direction = 0
                    if self.service_list:
                        self.direction = 1
                        for userRequest in range(self.on_floor, max(self.service_list) + 1):
                            self.on_floor = userRequest
                            self.commonFunForRequestProcess(userRequest)
                            if not self.service_list:
                                break
                    self.direction = 0
                if not self.service_list:
                    break
        SQL = """ 
                  update  elevator_floorrequest   set archived_at=%s where lift_id=%s          
              """
        cursor = connection.cursor()
        cursor.execute(SQL, (datetime.datetime.now(), self.lift_number,))
        connection.commit()
        connection.close()
        self.elevatorServiceDirection(True)
