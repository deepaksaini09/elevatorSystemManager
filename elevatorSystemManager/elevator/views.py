import io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .elevatorSystem.elevatorsSystem import ElevatorsSystem
from .serializers import elevatorSerializers, floorRequestSerializers, elevatorAndFloorSerializedData, \
    elevatorMovingUpOrDownSerializers, elevatorDoorStatusSerializers, elevatorIsMaintenanceStatusSerializers, \
    saveUserRequestForElevators
from django.db import connection
from .models import Elevator


@csrf_exempt
def initializeElevatorSystem(request):
    """ initialising new elevator
      param - numberOfElevator(taking integer parameter number of elevator)
     """
    try:
        if request.method == 'POST':
            body = request.body
            stream = io.BytesIO(body)
            pythonData = JSONParser().parse(stream)
            getElevatorNumber = pythonData['numberOfElevator']
            numberOfElevatorsExist = Elevator.objects.all()
            totalInitializeElevators = getElevatorNumber - len(numberOfElevatorsExist)
            if totalInitializeElevators <= 0:
                return JsonResponse({"message": "invalid elevator number or same elevator already exist"})
            numbersOfElevators = [Elevator(lift_number=elevatorSequence) for elevatorSequence in
                                  range(len(numberOfElevatorsExist) + 1, getElevatorNumber + 1)]
            try:
                data = Elevator.objects.bulk_create(numbersOfElevators)
                if data:
                    return JsonResponse({"message": 'initialize new elevators'})
            except Exception as error:
                return JsonResponse({"message": 'error initialize new elevators ' + str(error)})
            return JsonResponse({'message': 'error during process request'})
        return JsonResponse({"message": 'request is invalid'})
    except Exception as error:
        print(error)
        return JsonResponse({"message": " error occurred during processing request " + str(error.args)})


@csrf_exempt
def getElevatorsUserRequest(request):
    """ getting user floor request for particular elevator """
    try:
        if request.method == 'POST':
            body = request.body
            stream = io.BytesIO(body)
            pythonData = JSONParser().parse(stream)
            getElevatorNumber = pythonData['elevatorID']
            cursor = connection.cursor()
            SQL = """ 
                    select lift_number, is_operational, is_maintenance, is_available, current_floor, is_upward, moving_up, 
                           id, floor_number, is_door_close_open, archived_at, lift_id
                    from elevator_elevator e
                             join elevator_floorrequest f on e.lift_number = f.lift_id
                    
                    where e.lift_number = %s
                    
                  """
            cursor.execute(SQL, (getElevatorNumber,))
            elevatorDetails = cursor.fetchall()
            columnName = ['lift_number', 'is_operational', 'is_maintenance', 'is_available', 'current_floor',
                          'is_upward'
                , 'moving_up', 'floor_number', 'is_door_close_open', 'archived_at', 'lift_id']
            elevatorMapDetails = [dict(zip(columnName, elevatorDetail)) for elevatorDetail in elevatorDetails]
            print(elevatorMapDetails)
            serializer = elevatorAndFloorSerializedData(data=elevatorMapDetails, many=True)
            serializer.is_valid()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({"message": " invalid method " + str(request.method)})
    except Exception as error:
        print(error)
        return JsonResponse({"message": " error occurred during processing request " + str(error.args)})


@csrf_exempt
def getLiftIsMovingOrNot(request):
    """ getting details of a particular elevator it is moving or not or in rest """
    try:
        if request.method == 'POST':
            body = request.body
            stream = io.BytesIO(body)
            pythonData = JSONParser().parse(stream)
            getElevatorNumber = pythonData['elevatorID']
            # elevatorsMovingOrDownDetails = Elevator.objects.filter(lift_number=getElevatorNumber)
            cursor = connection.cursor()
            SQL = """ 
                      select lift_number, moving_up from elevator_elevator where lift_number=%s
                  """
            cursor.execute(SQL, (getElevatorNumber,))
            elevatorDetails = cursor.fetchall()
            columnName = ['lift_number', 'moving_up']
            elevatorMapDetails = [dict(zip(columnName, elevatorDetail)) for elevatorDetail in elevatorDetails]
            serializer = elevatorMovingUpOrDownSerializers(data=elevatorMapDetails, many=True)
            if serializer.is_valid():
                return JsonResponse(serializer.data, safe=False)
            return JsonResponse({"message": 'not found valid data' + str(serializer.error_messages)})
        else:
            return JsonResponse({"message": " invalid method " + str(request.method)})
    except Exception as error:
        print(error)
        return JsonResponse({"message": " error occurred during processing request " + str(error.args)})


@csrf_exempt
def getElevatorDoorStatus(request):
    """ this is used for getting particular elevator door status
        0 - door is closed
        1- door is open
    """
    try:
        if request.method == 'POST':
            body = request.body
            stream = io.BytesIO(body)
            pythonData = JSONParser().parse(stream)
            getElevatorNumber = pythonData['elevatorID']
            elevatorsMovingOrDownDetails = Elevator.objects.filter(lift_number=getElevatorNumber)
            cursor = connection.cursor()
            SQL = """ 
                      select lift_number,is_door_close_open from elevator_elevator where lift_number=%s
                  """
            cursor.execute(SQL, (getElevatorNumber,))
            elevatorDetails = cursor.fetchall()
            print(elevatorDetails)
            connection.close()
            columnName = ['lift_number', 'is_door_close_open']
            elevatorMapDetails = [dict(zip(columnName, elevatorDetail)) for elevatorDetail in elevatorDetails]
            serializer = elevatorDoorStatusSerializers(data=elevatorMapDetails, many=True)
            if serializer.is_valid():
                return JsonResponse(serializer.data, safe=False)
            return JsonResponse({"message": 'not found valid data' + str(serializer.error_messages)})
        else:
            return JsonResponse({"message": " invalid method " + str(request.method)})
    except Exception as error:
        print(error)
        return JsonResponse({"message": " error occurred during processing request " + str(error.args)})


@csrf_exempt
def getElevatorNextDestination(request):
    try:
        if request.method == 'POST':
            body = request.body
            stream = io.BytesIO(body)
            pythonData = JSONParser().parse(stream)
            getElevatorNumber = pythonData['elevatorID']
            cursor = connection.cursor()
            SQL = """ 
                              select lift_number, moving_up, current_floor from elevator_elevator where lift_number=%s
                          """
            cursor.execute(SQL, (getElevatorNumber,))
            elevatorDetails = cursor.fetchone()
            floorStatus = elevatorDetails[2]
            if elevatorDetails[1] == 1:
                if floorStatus < 12:  # 12 is maximum floor
                    floorStatus += 1
            elif elevatorDetails[1] == -1:  # -4 is minimum floor
                if floorStatus > -4:
                    floorStatus -= 1
            return JsonResponse(f"next floor destination is : {floorStatus}")
        else:
            return JsonResponse({"message": " invalid method " + str(request.method)})

    except Exception as error:
        return JsonResponse({"message": 'error to finding next request' + str(error.args)})


@csrf_exempt
def markElevatorInMaintenance(request):
    """ this is used for mark elevator is in isMaintenance or not
        params -
             elevatorID - elevator number
             isMaintenance - is boolean value
                             0 or False not under maintenance
                             1 or True - under maintenance

    """
    try:
        if request.method == 'POST':
            body = request.body
            stream = io.BytesIO(body)
            pythonData = JSONParser().parse(stream)
            getElevatorNumber = pythonData['elevatorID']
            isMaintenance = pythonData['isMaintenance']
            cursor = connection.cursor()
            SQL = """ 
                      update  elevator_elevator set is_maintenance=%s where lift_number=%s
                  """
            cursor.execute(SQL, (isMaintenance, getElevatorNumber))
            connection.commit()
            SQL = """ select lift_number, is_maintenance from elevator_elevator where lift_number=%s"""
            cursor.execute(SQL, (getElevatorNumber,))
            elevatorDetails = cursor.fetchall()
            print(elevatorDetails)
            connection.close()
            columnName = ['lift_number', 'is_maintenance']
            elevatorMapDetails = [dict(zip(columnName, elevatorDetail)) for elevatorDetail in elevatorDetails]
            serializer = elevatorIsMaintenanceStatusSerializers(data=elevatorMapDetails, many=True)
            if serializer.is_valid():
                return JsonResponse(serializer.data, safe=False)
            return JsonResponse({"message": 'not found valid data' + str(serializer.error_messages)})
        else:
            return JsonResponse({"message": " invalid method " + str(request.method)})
    except Exception as error:
        print(error)
        return JsonResponse({"message": " error occurred during processing request " + str(error.args)})


def commonFunctionForGettingAllDetailsOfElevators():
    """ this common function is used to get all floor request and their all details
       param -
         moving_up- it used for direction of elevator
         current_floor - it is used for current floor of elevator
         floor_number - it is used for floors request

    """
    try:
        cursor = connection.cursor()
        SQL = """
                                select lift_number, is_operational, is_maintenance, is_available, current_floor, is_upward, moving_up,
                                       id, floor_number, is_door_close_open, archived_at, lift_id
                                from elevator_elevator e
                                         join elevator_floorrequest f on e.lift_number = f.lift_id
                                where archived_at is null and is_maintenance=0
                      """
        cursor.execute(SQL)
        elevatorDetails = cursor.fetchall()
        if not elevatorDetails:
            return False
        columnName = ['lift_number', 'is_operational', 'is_maintenance', 'is_available', 'current_floor', 'is_upward'
            , 'moving_up', 'id', 'floor_number', 'is_door_close_open', 'archived_at', 'lift_id']
        elevatorMapDetails = [dict(zip(columnName, elevatorDetail)) for elevatorDetail in elevatorDetails]
        print(elevatorMapDetails)
        elevatorsDetailsInMap = {}
        for elevatorsDetail in elevatorMapDetails:
            if elevatorsDetail['lift_number'] not in elevatorsDetailsInMap:
                elevatorsDetailsInMap[elevatorsDetail['lift_number']] = [elevatorsDetail['moving_up'],
                                                                         elevatorsDetail['current_floor'],
                                                                         [elevatorsDetail['floor_number']],
                                                                         ]
            else:
                elevatorsDetailsInMap[elevatorsDetail['lift_number']][2].append(elevatorsDetail['floor_number'])
        return elevatorsDetailsInMap

    except Exception as error:
        print(error)


@csrf_exempt
def savesUsersRequestForElevator(request):
    """ saves user floor request for  and also assign most optimal elevator
      param - usersRequest(this array of floor request)
    """
    try:
        if request.method == 'POST':
            elevatorsDetailsInMap = commonFunctionForGettingAllDetailsOfElevators()
            body = request.body
            stream = io.BytesIO(body)
            pythonData = JSONParser().parse(stream)
            userRequestsList = pythonData['usersRequest']
            elevatorsSystemObject = ElevatorsSystem(elevatorsDetailsInMap)
            distance = None
            for userRequests in userRequestsList:
                sortedMap = {}
                for particularElevator in elevatorsSystemObject.elevators:
                    print(particularElevator.service_list, particularElevator.on_floor, particularElevator.direction)
                    if particularElevator.direction == 1:
                        distance = abs((max([
                                                0] if not particularElevator.service_list else particularElevator.service_list) - userRequests) + (
                                               max([
                                                       0] if not particularElevator.service_list else particularElevator.service_list) - particularElevator.on_floor))
                        # print(distance)
                    elif particularElevator.direction == 0:
                        particularElevator.direction = 1
                        if userRequests < particularElevator.on_floor:
                            particularElevator.direction = -1
                        print(particularElevator.service_list)
                        distance = abs(max([
                                               0] if not particularElevator.service_list else particularElevator.service_list) - particularElevator.on_floor)
                    elif particularElevator.direction == -1:
                        distance = abs((min([
                                                0] if not particularElevator.service_list else particularElevator.service_list) - userRequests) + (
                                               min([
                                                       0] if not particularElevator.service_list else particularElevator.service_list) - particularElevator.on_floor))
                    sortedMap[particularElevator] = distance
                print(sortedMap, userRequests)
                for w in sorted(sortedMap, key=sortedMap.get):
                    print(w.service_list, w.lift_number)
                    print(w.service_list)
                    if userRequests not in w.service_list:
                        print(particularElevator.service_list)
                        w.service_list.append(userRequests)
                        print(sortedMap[w], 'j', userRequests)
                        serializersObj = saveUserRequestForElevators(data={'floor_number': userRequests,
                                                                           'lift_id': w.lift_number
                                                                           })
                        if serializersObj.is_valid():
                            serializersObj.save()
                            print(
                                f' floor is : {userRequests} and mapped with{particularElevator.lift_number} Elevator')
                        else:
                            print(
                                f' error occurred during mapping floor is : {sortedMap[w]} and mapped with this {particularElevator.lift_number} Elevator')
                        break
        else:
            return JsonResponse({"message": " invalid method " + str(request.method)})

    except Exception as error:
        print(error)
        return JsonResponse({"message": 'process user request ' + str(error.args)})


def runElevators(request):
    """ run all elevator for processing it all their services """
    try:
        if request.method == 'GET':
            elevatorsDetailsInMap = commonFunctionForGettingAllDetailsOfElevators()
            if not elevatorsDetailsInMap:
                return JsonResponse({"message": "no user request is remaining"})
            elevatorsSystemObject = ElevatorsSystem(elevatorsDetailsInMap)
            for elevatorsObject in elevatorsSystemObject.elevators:
                print(elevatorsObject.processRequest())
            return JsonResponse({'message': 'elevators has been processed their request'})
        else:
            return JsonResponse({"message": " invalid method " + str(request.method)})
    except Exception as error:
        print(error)
        return JsonResponse({"message": " error occurred during processing request " + str(error.args)})
