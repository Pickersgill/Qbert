module Events exposing (..)

import Json.Decode exposing (..)
import Debug exposing (log, toString)
import List exposing (filter, map, maximum, range, drop)
import Dict exposing (..)
import Tuple exposing (pair)

type alias Pos = {x : Float, y : Float}
type Service = Green | Red | Blue | Orange | Yellow | Purple | BadColour

type alias AgentID = Int
type alias KioskID = Int
type alias TaskID = Int
type alias Time = Int

type Event = AgentCreatedEvent Time AgentID Pos
           | KioskCreatedEvent Time KioskID Pos Service Int Int
           | TurnEvent Time AgentID Float
           | MoveEvent Time AgentID Pos
           | CompleteTaskEvent Time AgentID TaskID
           | AssignTaskEvent Time TaskID AgentID Service Int
           | JoinQueueEvent Time AgentID KioskID
           | LeaveQueueEvent Time AgentID KioskID
           | FailQueueEvent Time AgentID
           | BadEvent String

type alias EventList = List (Event)
type alias EventTimeDict = Dict Int EventList

bucketByTime : EventList -> Dict Int EventList
bucketByTime events =
    let
        maxTime = getMaxTime events
    in Dict.fromList (getBucketPairs 0 (maxTime) events)

getBucketPairs : Int -> Int -> EventList -> List (Int, EventList)
getBucketPairs start end events =
    if start > end then []
    else
        let
            en = filterByTime events start
        in (start, en) ::
           getBucketPairs (start + 1)
                          (end)
                          (drop (List.length en) events)
                          

getMaxTime : EventList -> Int
getMaxTime events =
    let 
        max = maximum (List.map (\e -> getEventTime e) events)
    in case max of
        Just val -> val
        Nothing -> 0

filterByTime : EventList -> Int -> EventList
filterByTime events t = 
        fastFilter (\f -> hasTimeLessThan f t) (\e -> hasTime e t) events

fastFilter : (a -> Bool) -> (a -> Bool) -> List a -> List a
fastFilter skip include list =
    let
        head = List.head list
        tail = safeTail list
    in case head of
        Just value ->
            if skip value then fastFilter skip include tail
            else if include value then value :: fastFilter skip include tail
            else []
        Nothing -> []
    

partitionByTime : EventList -> Int -> (EventList, EventList)
partitionByTime events t = List.partition (\e -> hasTime e t) events

hasTimeLessThan : Event -> Int -> Bool
hasTimeLessThan event t =
    getEventTime event < t

hasTime : Event -> Int -> Bool
hasTime event t = getEventTime event == t

safeTail : List a -> List a
safeTail l =
    let
        t = List.tail l
    in case t of
        Just v -> v
        Nothing -> []

getEventTime : Event -> Int
getEventTime event =
    case event of
        AgentCreatedEvent t _ _ -> t
        KioskCreatedEvent t _ _ _ _ _ -> t
        TurnEvent t _ _ -> t
        MoveEvent t _ _ -> t
        CompleteTaskEvent t _ _ -> t
        AssignTaskEvent t _ _ _ _ -> t
        JoinQueueEvent t _ _ -> t
        LeaveQueueEvent t _ _ -> t
        FailQueueEvent t _ -> t
        BadEvent _ -> -1
        
serviceToColour : Service -> String
serviceToColour service =
    case service of
        Green -> "Green"
        Red -> "Red"
        Blue -> "Blue"
        Yellow -> "Yellow"
        Orange -> "Orange"
        Purple -> "Purple"
        BadColour -> "Black"


-- DECODERS

eventListDecoder : Decoder EventList
eventListDecoder =
 Json.Decode.list((field "event" string) |> Json.Decode.andThen eventDecoder)

eventDecoder : String -> Decoder Event
eventDecoder eventStr = 
    case eventStr of
      
      "AGENT_CREATED" -> agentCreatedEventDecoder
      "KIOSK_CREATED" -> kioskCreatedEventDecoder
      "MOVE_TO" -> moveEventDecoder
      "TURN_TO" -> turnEventDecoder
      "FAIL_QUEUE" -> failQueueEventDecoder
      "JOIN_QUEUE" -> joinQueueEventDecoder
      "LEAVE_QUEUE" -> leaveQueueEventDecoder
      "ASSIGN_TASK" -> assignTaskEventDecoder
      "COMPLETE_TASK" -> completeTaskEventDecoder
      _ -> Json.Decode.map BadEvent (field "event" string)
      

agentCreatedEventDecoder : Decoder Event
agentCreatedEventDecoder = Json.Decode.map3 AgentCreatedEvent (field "time" int)
                                                              (field "agent_id" int)
                                                            (field "pos" posDecoder)

kioskCreatedEventDecoder : Decoder Event
kioskCreatedEventDecoder = 
  Json.Decode.map6 KioskCreatedEvent (field "time" int)
                                     (field "kiosk_id" int)
                                     (field "pos" posDecoder)
                                     (Json.Decode.andThen serviceDecoder 
                                        (field "service" string))
                                     (field "servers" int)
                                     (field "service_time" int)

turnEventDecoder : Decoder Event
turnEventDecoder = 
  Json.Decode.map3 TurnEvent (field "time" int)
                             (field "agent" int)
                             (field "direction" float)

moveEventDecoder : Decoder Event
moveEventDecoder = 
  Json.Decode.map3 MoveEvent (field "time" int)
                             (field "agent" int)
                             (field "pos" posDecoder)

assignTaskEventDecoder : Decoder Event
assignTaskEventDecoder = 
  Json.Decode.map5 AssignTaskEvent (field "time" int)
                                   (field "task" int)
                                   (field "agent" int)
                                   (Json.Decode.andThen serviceDecoder
                                      (field "service" string))
                                   (field "priority" int)

completeTaskEventDecoder : Decoder Event
completeTaskEventDecoder = 
  Json.Decode.map3 CompleteTaskEvent (field "time" int)
                                     (field "agent" int)
                                     (field "task" int)

joinQueueEventDecoder : Decoder Event
joinQueueEventDecoder = 
  Json.Decode.map3 JoinQueueEvent (field "time" int)
                                  (field "agent" int)
                                  (field "kiosk" int)

leaveQueueEventDecoder : Decoder Event
leaveQueueEventDecoder =
  Json.Decode.map3 LeaveQueueEvent (field "time" int)
                                   (field "agent" int)
                                   (field "kiosk" int)

failQueueEventDecoder : Decoder Event
failQueueEventDecoder = 
  Json.Decode.map2 FailQueueEvent (field "time" int)
                                  (field "agent" int)

serviceDecoder : String -> Decoder Service
serviceDecoder service_str =
  case service_str of
  "GREEN" -> Json.Decode.succeed Green
  "RED" -> Json.Decode.succeed Red
  "ORANGE" -> Json.Decode.succeed Orange
  "BLUE" -> Json.Decode.succeed Blue
  "PURPLE" -> Json.Decode.succeed Purple
  "YELLOW" ->Json.Decode.succeed Yellow
  _ -> Json.Decode.succeed BadColour

posDecoder : Decoder Pos
posDecoder = Json.Decode.map2 Pos (index 0 float) (index 1 float)

