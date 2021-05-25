module Tasks exposing (..)

import List exposing (head, filter)
import Events exposing (..)

type alias Task = 
    {id : Int, service : Service, priority : Int}

type alias TaskList = List Task

getTask : Int -> TaskList -> Maybe Task
getTask id tasks =
    head (filter (\t -> (hasID t id)) tasks)

hasID : Task -> Int -> Bool
hasID task id = task.id == id
