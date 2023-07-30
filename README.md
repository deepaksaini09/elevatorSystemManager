# Assumption
1. first providing user floor request and initialising n elevator .
2. door status - door open parameter (1 or True)
               - door close parameter (0 or False)
3. elevator downward or upward status - 1 (going upward)
                                      - 0 (in rest)
                                      - -1(going downward)


# steps to run project(1-3) 
1. initialise project with 'numberOfElevator' parameter in body and here we have to pass number of elevator for 
   initialising(default status of elevator door is closed and elevator is in rest).
   ### API end point 
    1. '/initializeElevatorSystem' and method  POST  
    2. body parameter - numberOfElevator(integer number)
2. initialising user floor request with optimal elevator.
    ### API end point  
    1. '/savesUsersRequestForElevator' and method  POST  
    2. body parameter - usersRequest(array)
3. run project .
     ### API end point
     1. '/runElevators' and method GET


# additional API End Point 
1. mark elevator is maintenance or not.
   ### API end point
   1. '/markElevatorInMaintenance' and method POST
   2. body parameter - 
      1. elevatorID - elevator ID 
      2. isMaintenance - pass boolean value 0- not in maintenance , 1-  in maintenance
   
2. getting elevator door status for a particular elevator 
   ### API end point
   1. '/getElevatorDoorStatus' and method POST 
   2. body parameter - 
      1. elevatorID - elevator ID 

3. getting elevator Moving direction status for a particular elevator 
   ### API end point
   1. '/getLiftIsMovingOrNot' and method POST
   2. body parameter - 
      1. elevatorID - elevator ID 
   
4. getting elevator user floor request status for a particular elevator 
   ### API end point
   1. '/getElevatorsUserRequest' and method POST
   2. body parameter - 
      1. elevatorID - elevator ID

5. getting elevator next destination of elevator for a particular elevator 
   ### API end point
   1. '/getElevatorNextDestination' and method POST
   2. body parameter - 
      1. elevatorID - elevator ID


   
