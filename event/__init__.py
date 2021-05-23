try:
    import eventLogger
    import eventClasses
except:
    from . import eventLogger
    from . import eventClasses

EventLogger = eventLogger.EventLogger

CompleteTaskEvent = eventClasses.CompleteTaskEvent
AssignTaskEvent = eventClasses.AssignTaskEvent
MoveEvent = eventClasses.MoveEvent
TurnEvent = eventClasses.TurnEvent
JoinQueueEvent = eventClasses.JoinQueueEvent
LeaveQueueEvent = eventClasses.LeaveQueueEvent
FailQueueEvent = eventClasses.FailQueueEvent
CreateKioskEvent = eventClasses.CreateKioskEvent
CreateAgentEvent = eventClasses.CreateAgentEvent
