from abc import ABCMeta, abstractmethod
from datetime import datetime

from typing import Optional, List


class NewTask:
    """ TaskTuple

    A TaskTuple represents the feature rich mechanism for notifications, alerts and messages
     sent from initiator plugins to mobile devices.

    """

    # Auto complete options
    AUTO_COMPLETE_OFF = 0
    AUTO_COMPLETE_ON_DELIVER = 1
    AUTO_COMPLETE_ON_SELECT = 2
    AUTO_COMPLETE_ON_ACTION = 4

    # Auto delete options
    AUTO_DELETE_OFF = 0
    AUTO_DELETE_ON_DELIVER = 1
    AUTO_DELETE_ON_SELECT = 2
    AUTO_DELETE_ON_ACTION = 4
    AUTO_DELETE_ON_COMPLETE = 8

    # notification mask (multiple options allowed)
    NOTIFY_BY_DEVICE_POPUP = 1
    NOTIFY_BY_DEVICE_SOUND = 2
    NOTIFY_BY_SMS = 4
    NOTIFY_BY_EMAIL = 8

    # Display options
    DISPLAY_AS_TASK = 0
    DISPLAY_AS_MESSAGE = 1

    def __init__(self, uniqueId: str, userId: str, title: str,
                 description: Optional[str] = None, iconPath: Optional[str] = None,
                 displayAs:int = 0,
                 routePath: Optional[str] = None, routeParamJson: Optional[dict] = None,
                 autoComplete: int = 0, autoDelete: int = 0,
                 onDeliveredPayload: Optional[bytes] = None,
                 onCompletedPayload: Optional[bytes] = None,
                 onDeletedPayload: Optional[bytes] = None,
                 notificationRequiredFlags: int = 0,
                 actions: List['NewTaskAction'] = ()):
        """
        :param uniqueId: A unique identifier provided when this task was created.
            The initiating plugin may use this later to cancel the task.
            HINT : Ensure you prefix the uniqueId with your plugin name.
    
        :param userId: A string representing the unique ID of the user. This must match the
            users plugin.
    
        :param title: The title to display in the task.
        :param description: The long text that is displayed under the title for this task.
        :param iconPath: The URL for the icon, if any.
        :param displayAs: Should this task be displayed as a message or task?
    
        :param routePath: If this route path is defined, then selecting the task
            will cause the peek client fe to change routes to a new page.
        :param routeParamJson: If the route path is defined, this route param json 
            will be passed along when the route is switched..
    
        :param autoComplete: Should this task auto complete?
                This parameter defines what state it will auto complete in.
                See the AUTO_COMPLETE... class constants
        :param autoDelete: Should this task auto delete?
                This parameter defines what state it will auto delete in.
                See the AUTO_DELETE... class constants
    
        :param onDeliveredPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the task is delivered.
        :param onCompletedPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the task is completed (auto, or otherwise)
        :param onDeletedPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the task is deleted (auto, or otherwise)
        """
        self.uniqueId = self._required(uniqueId, "uniqueId")
        self.userId = self._required(userId, "userId")

        # The display properties of the task
        self.title = self._required(title, "title")
        self.description = description
        self.iconPath = iconPath

        self.displayAs = displayAs

        # The client_fe_app route to open when this task is selected
        self.routePath = routePath
        self.routeParamJson = routeParamJson

        # The confirmation options
        self.onDeliveredPayload = onDeliveredPayload
        self.onCompletedPayload = onCompletedPayload
        self.onDeletedPayload = onDeletedPayload

        self.autoComplete = autoComplete
        self.autoDelete = autoDelete

        self.notificationRequiredFlags = notificationRequiredFlags

        # The actions for this TaskTuple.
        self.actions = list(actions)

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class NewTaskAction:
    """ TaskTuple Action

    This object represents the TaskTuple Actions.
    Tasks have zero or more actions that can be performed by the user when they
    receive a task.

    """

    def __init__(self, title: str, confirmMessage: str,
                 onActionPayload: Optional[bytes] = None):
        """
        :param title: The title of the action, this will appear as a menu option.
        :param confirmMessage: This is the message that will be shown to confirm the action.
        :param onActionPayload: This payload will be delivered locally on Peek Server
                 When the action is performed on the user device.
        """
        self.title = self._required(title, "title")
        self.confirmMessage = self._required(confirmMessage, "confirmMessage")
        self.onActionPayload = self._required(onActionPayload, "onActionPayload")

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class NewActivity:
    """ TaskTuple

    A TaskTuple represents the feature rich mechanism for notifications, alerts and messages
     sent from initiator plugins to mobile devices.

    """

    def __init__(self, uniqueId: str, userId: str, title: str,
                 dateTime: Optional[datetime] = None,
                 description: Optional[str] = None, iconPath: Optional[str] = None,
                 routePath: Optional[str] = None, routeParamJson: Optional[dict] = None,
                 autoDeleteDateTime: Optional[datetime] = None):
        """

        :param uniqueId: A unique identifier provided when this task was created.
            The initiating plugin may use this later to cancel the task.
            HINT : Ensure you prefix the uniqueId with your plugin name.
    
        :param userId: A string representing the unique ID of the user. This must match the
            users plugin.
    
        :param title: The title to display in the task.
        :param description: The long text that is displayed under the title for this task.
        :param iconPath: The URL for the icon, if any.
    
        :param routePath: If this route path is defined, then selecting the task
            will cause the peek client fe to change routes to a new page.
        :param routeParamJson: If the route path is defined, this route param json 
            will be passed along when the route is swtiched.
            
        :param autoDeleteDateTime: The time and date when this activity will be deleted.
        
        """
        self.uniqueId = self._required(uniqueId, "uniqueId")
        self.userId = self._required(userId, "userId")
        self.dateTime = dateTime if dateTime else datetime.utcnow()

        # The display properties of the task
        self.title = self._required(title, "title")
        self.description = description
        self.iconPath = iconPath

        # The client_fe_app route to open when this item is selected
        self.routePath = routePath
        self.routeParamJson = routeParamJson

        # Auto Delete on Time
        self.autoDeleteDateTime = autoDeleteDateTime

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class ActiveTaskApiABC(metaclass=ABCMeta):
    @abstractmethod
    def addTask(self, task: NewTask) -> None:
        """ Add a New Task

        Add a new task to the users device.
        
        :param task: The definition of the task to add.
        
        """

    @abstractmethod
    def completeTask(self, uniqueId: str) -> None:
        """ Complete a Task
        
        Mark a task as complete. NOTE, This doesn't delete it.
        
        :param uniqueId: The uniqueId provided when the task was created.
        """

    @abstractmethod
    def removeTask(self, uniqueId: str) -> None:
        """ Remove a Task
        
        Remove a task from the users device.
        
        :param uniqueId: The uniqueId provided when the task was created.
        """

    @abstractmethod
    def addActivity(self, activity: NewActivity) -> None:
        """ Add a new Activity item

        Add a new Activity to the users device.

        :param activity: The definition of the activity to add.

        """

    @abstractmethod
    def removeActivity(self, uniqueId: str) -> None:
        """ Remove an Activity item

        Remove an Activity from the users device.

        :param uniqueId: The uniqueId provided when the activity was created.
        """
