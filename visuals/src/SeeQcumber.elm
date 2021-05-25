module SeeQcumber exposing (..)

import Browser
import Debug exposing (log, toString)
import File exposing (..)
import Task exposing (..)
import File.Select as Select
import Json.Decode exposing (..)
import Html exposing (..)
import Dict exposing (..)
import List exposing (..)
import Time exposing (..)
import Tuple exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Browser.Events exposing(onAnimationFrame)
import Svg exposing (svg, rect)
import Svg.Attributes as SA exposing (..)
import Events exposing (..)
import Tasks exposing (..)
import Agents exposing (..)
import Color exposing (..)

-- MAIN


main =
  Browser.element
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    }

-- MODEL

type alias JSON = String

type alias Env = {width : Int, height : Int, time_limit : Int}

type Log = Log Env Events.EventList

type alias EnvState =
  {pause : Bool, time : Int, agents : AgentList}

type alias Play = Bool
type Model = Empty 
            | Loading File
            | Loaded JSON
            | Ready Log EnvState


init : () -> (Model, Cmd Msg)
init _ = 
    (Empty, Cmd.none)
  

-- UPDATE

type Msg = ChooseFile
         | FileChosen File
         | FileLoaded String
         | NextFrame Posix
         | PlayPause


update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    ChooseFile ->
      (model, Select.file ["application/json"] FileChosen)
    FileChosen file ->
      (Loading file, Task.perform FileLoaded (File.toString file))
    FileLoaded log_str ->
      let
        log = (decodeString logDecoder log_str)
      in case log of
        Err _ -> (Empty, Cmd.none)
        Ok value -> ((Ready value (EnvState True 0 [])), Cmd.none)
    NextFrame time -> (updateTime model |> doEvents, Cmd.none)
    PlayPause -> case model of
        Ready log state -> (Ready log {state | pause = not state.pause}, Cmd.none)
        _ -> (model, Cmd.none)

updateTime : Model -> Model
updateTime model =
  case model of
    Ready log state -> 
      case state.pause of
        False -> Ready log {state | time = state.time + 1}
        _ -> model
    _ -> model

doEvents : Model -> Model
doEvents model = 
  case model of
    Ready (Log env events) state -> 
      let 
        eventSets = partitionByTime events state.time
        eventsTodo = first eventSets
        remEvents = second eventSets
      in Ready (Log env remEvents) (performEvents state eventsTodo)

    _ -> model

performEvents : EnvState -> EventList -> EnvState
performEvents state events = 
  List.foldl (doEvent) state events

doEvent : Events.Event -> EnvState -> EnvState
doEvent event state = 
  case event of 
    AgentCreatedEvent _ id pos -> 
      let
        colour = Color.rgb255 230 120 10
        dir = 0
        tasks = []
      in
        {state | agents = (Agent id pos dir colour tasks) :: state.agents}
    MoveEvent _ id pos ->
      {state | agents = moveAgent id pos state.agents}

    _ -> state

-- SUBSCRIPTIONS

subscriptions : Model -> Sub Msg
subscriptions model =
  onAnimationFrame NextFrame

-- VIEW

view : Model -> Html Msg
view model =
  case model of

    Empty -> div [] [uploadButton]
  
    Loading file -> div [] [text "loading"]

    Loaded file -> div [] [text file]

    Ready (Log env events) state ->
        div [] [ 
          pre [] [
            text ("Events Remaining: " ++ (String.fromInt (List.length events)))
          , text ("\nTime: " ++ String.fromInt state.time)
          ]
        , envCanvas env state
        , playButton state.pause
        ]


playButton paused = 
  case paused of
    True -> button [onClick PlayPause] [text "Play"]
    False -> button [onClick PlayPause] [text "Pause"]

envCanvas env state = 
  let
    w = String.fromInt env.width
    h = String.fromInt env.height
  in
    svg [SA.width w, SA.height h, fill "Black"] 
        (List.append [ rect [
                          x "0", y "0", 
                          SA.width w, 
                          SA.height h,
                          SA.fill "Gray",
                          SA.stroke "Black"
                        ] [] ]
        (List.map agentDot state.agents))

agentDot : Agent -> Svg.Svg msg
agentDot agent = 
  let
    x = String.fromFloat agent.pos.x
    y = String.fromFloat agent.pos.y
    col = Color.toCssString agent.colour
  in
  Svg.circle [cx x, cy y, fill col, stroke "black", r "5"] []

getEventText : Events.EventList -> String
getEventText events = Debug.toString events

uploadButton = button [onClick ChooseFile] [text "Upload a log file"]

-- DECODERS

logDecoder : Decoder Log
logDecoder = Json.Decode.map2 Log 
             (field "env" envDecoder)
             (field "events" eventListDecoder)

envDecoder : Decoder Env
envDecoder = Json.Decode.map3 Env (field "width" int) 
                                  (field "height" int)
                                  (field "time_limit" int)

