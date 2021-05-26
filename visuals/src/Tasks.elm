module Tasks exposing (..)

import List exposing (head, filter, map)
import Events exposing (..)

type alias Task = 
    {id : Int, service : Service, priority : Int, complete : Bool}

type alias TaskList = List Task

getTask : Int -> TaskList -> Maybe Task
getTask id tasks =
    head (filter (\t -> (hasID t id)) tasks)

makeComplete : Int -> TaskList -> TaskList
makeComplete id tasks = 
    map (\t -> if (hasID t id) then {t | complete = True} else t) tasks
    

hasID : Task -> Int -> Bool
hasID task id = task.id == id
