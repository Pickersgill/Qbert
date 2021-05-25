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
    map (\a -> moveIfID a id newPos) agents

moveIfID : Agent -> Int -> Pos -> Agent
moveIfID agent id newPos =
    if hasID agent id then
        {agent | pos = newPos}
    else
        agent

hasID : Agent -> Int -> Bool
hasID agent id = agent.id == id
