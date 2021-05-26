module Kiosks exposing (..)

import List exposing (head, filter, map)
import Tasks exposing (..)
import Events exposing (..)
import Agents exposing (..)
import Color exposing (..)


type alias Kiosk = 
    {id : Int, entrance : Pos,  service : Service, servers : Int, serve_time : Int, servingAgents : AgentList}

type alias KioskList = List Kiosk

getKiosk : Int -> KioskList -> Maybe Kiosk
getKiosk id kiosks =
    head (filter (\k -> hasID k id) kiosks)

queueAgent : Int -> Int -> AgentList -> KioskList -> (AgentList, KioskList)
queueAgent agent kiosk agents kiosks = 
    let
        queueingAgent = getAgent agent agents
    in case queueingAgent of
        Just value -> 
            (leave agent agents, enqueue kiosk value kiosks)
        Nothing -> (agents, kiosks)

unqueueAgent : Int -> Int -> AgentList -> KioskList -> (AgentList, KioskList)
unqueueAgent agent kiosk agents kiosks = 
    let
        servedKiosk = getKiosk kiosk kiosks
    in case servedKiosk of
        Just kioskValue -> 
            let 
                servedAgent = getAgent agent kioskValue.servingAgents
            in case servedAgent of
                Just agentValue -> (
                    {agentValue | pos = kioskValue.entrance} :: agents
                  , unqueue kiosk agent kiosks)
                Nothing -> (agents, kiosks)
        Nothing -> (agents, kiosks)

unqueue : Int -> Int -> KioskList -> KioskList
unqueue kioskID agentID kiosks =
    map (\k -> if (hasID k kioskID) then 
            {k | servingAgents = leave agentID k.servingAgents}
            else k) kiosks

enqueue : Int -> Agent -> KioskList -> KioskList
enqueue kioskID agent kiosks =
    map (\k -> 
        if (hasID k kioskID) then {k | servingAgents = agent :: k.servingAgents}
        else k) kiosks

hasID : Kiosk -> Int -> Bool
hasID kiosk id = kiosk.id == id
