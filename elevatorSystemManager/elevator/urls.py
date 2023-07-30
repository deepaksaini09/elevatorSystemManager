from django.urls import path
from . import views

urlpatterns = [
    path('initializeElevatorSystem', views.initializeElevatorSystem),  # initialise elevator
    path('getElevatorsUserRequest', views.getElevatorsUserRequest),  # get user floor request
    path('getLiftIsMovingOrNot', views.getLiftIsMovingOrNot),  # getting elevator is moving or not
    path('getElevatorDoorStatus', views.getElevatorDoorStatus),  # getting elevator door status
    path('markElevatorInMaintenance', views.markElevatorInMaintenance),  # mark elevator maintenance
    path('runElevators', views.runElevators),  # run all elevator
    path('savesUsersRequestForElevator', views.savesUsersRequestForElevator),  # saving user floor elevator request
    path('getElevatorNextDestination', views.getElevatorNextDestination)  # find next destination of elevator
]
