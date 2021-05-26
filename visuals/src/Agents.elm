module Agents exposing (..)

import List exposing (head, filter, map)
import Tasks exposing (..)
import Events exposing (..)
import Color exposing (..)


type alias Agent = 
    {id : Int, pos : Pos, dir : Float, colour : Color, tasks : TaskList}

type alias AgentList = List Agent

getAgent : Int -> AgentList -> Maybe Agent
getAgent id agents =
    head (filter (\a -> hasID a id) agents)

moveAgent : Int -> Pos -> AgentList -> AgentList
moveAgent id newPos agents = 
    doIfID id (\a -> {a | pos = newPos}) agents

assignTask : Int -> Task -> AgentList -> AgentList
assignTask agentID task agents =
    doIfID agentID (\a -> {a | tasks = task :: a.tasks}) agents

completeTask : Int -> Int -> AgentList -> AgentList
completeTask agentID taskID agents =
    doIfID agentID (\a -> {a | tasks = (makeComplete taskID a.tasks)}) agents

remainingTasks : Agent -> Int
remainingTasks agent = List.length (filter (\t -> not t.complete) agent.tasks)

leave : Int -> AgentList -> AgentList
leave id agents =
    filter (\a -> not (hasID a id)) agents

doIfID : Int -> (Agent -> Agent) -> AgentList -> AgentList
doIfID id do agents = 
    map (\a -> if (hasID a id) then do a else a) agents

hasID : Agent -> Int -> Bool
hasID agent id = agent.id == id
