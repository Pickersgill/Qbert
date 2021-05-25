module Main exposing (..)

-- Press buttons to increment and decrement a counter.
--
-- Read how it works:
--   https://guide.elm-lang.org/architecture/buttons.html
--


import Browser
import List exposing (range)
import Html exposing (Html, button, div, text)
import Html.Events exposing (onClick)
import Svg exposing (..)
import Svg.Attributes exposing (..)



-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model = Int


init : Model
init =
  0



-- UPDATE


type Msg
  = Increment
  | Decrement
  | Double
  | Reset


update : Msg -> Model -> Model
update msg model =
  case msg of
    Increment ->
      model + 1

    Decrement ->
      model - 1

    Double ->
      model * 2
    
    Reset ->
      0



-- VIEW


view : Model -> Html Msg
view model =
    div []
    [ 
        button [ onClick Decrement ] [ Html.text "-" ]
        , div [] [ Html.text (String.fromInt model) ]
        , button [ onClick Increment ] [ Html.text "+" ]
        , button [ onClick Double ] [Html.text "*2" ]
        , button [ onClick Reset ] [Html.text "=0" ]
        , div []
        [
            svg [width "200", height "1000", fill "black"] 
            (get_dots model)
        ]
    ]

make_dot : Int -> (Svg Msg)
make_dot num =
    let 
        size = 10
        dim = 200
        offset = size
        pos = (num * 2 * size)
        x = offset + (modBy dim pos)
        y = (2 * offset) + (2 * size) * (pos // dim)
    in
    circle [ cx (String.fromInt x), 
             cy (String.fromInt y), 
             r "10" ] []

get_dots : Int -> List (Svg Msg)
get_dots dots =
    List.map make_dot (range 0 (dots - 1))

















