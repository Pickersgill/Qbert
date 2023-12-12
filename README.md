# Qbert
Simulation of task fulfilment by cognitive agents.

## Instructions For Building/Running QBert

### Dependencies

- Elm
- Python 3.8+

### Quickstart
To generate event logs use ```qbert/cleverMindTest.py```. This will use a pretty simple default mind
which targets the nearest (l2norm) kiosk for which it has a task.

There are some values in ```qbert/cleverMindTest.py``` which can be changed to affect number of agents,
number of tasks per agent, environment size, etc.

After running the simulation an event log file will be generated.

To visualiser is written in elm. You will need elm installed to build it.

Whilst in the ```visuals``` directory, use ```elm make src/SeeQcumber.elm```to build the webpage.
The webpage should be output in ```visuals/index.html```. Open the webpage and use the button to import
the ```event_log.json``` generated by qbert (see beginning of this section) then press play.

## The Problem

What's going on? The scenario:

    + N agents want to complete their tasks.
    + Each task can only be completed by a kiosk.
    + Each kiosk has a finite number of servers a server is occupied whilst the task is being completed.

So given this problem, how long do the agents take to complete their tasks on average? As a whole? Minimum? Maximum (Makespan)?

AND

What tpyes of agent behaviour might be good for minimising these metrics?

## The Solution

To simulate this problem we first need to define some physics:
    + The agents are situated in a bounded 2-dimensional plane.
    + Time moves in discrete unit steps. We called these Unit Time Steps, UTS.
    + After each UTS the agent receives a set of observations from the environment.
    + Using the observations, and any stored knowledge, the agent chooses to act. Either turning on the spot or moving forwards a short distance.

Okay, so we have defined the mechanism by which agents can move around and make decisions, but how do they complete tasks?

Each task may only be completed by a single kiosk, although a kiosk may have many servers. The kiosks are located, physically, around the perimeter of the environment. When an agent enters a kiosk, if they have a task for
that kiosk they may join the queue. Even if the kiosk is empty the agent must first join the queue and then be served at the beginning of the next UTS. Once the kiosk serves the agent they are free to join the queue again
immediately, or continue moving around.

The simulation is ended when:
    + No tasks remain
    + No agents are queueing

### Changing and Observing Agents

The behaviour of agents is determined by a Mind. Each mind has:
    + Some persistent beliefs in the form of attributes.
    + A revise function which iterates the beliefs based on observations from the environment.
    + A decide function which chooses an action to take based on the beliefs.

The simulator produces output logs in the form of ordered discrete time events. Theses events are used to reconstruct the execution and visualise the positions of the agents, remaining jobs and queue lengths.

### Technical Footnotes

The environment requests each agent action in sequence but does not apply the side effects of their actions until after ALL agents have given their choices. The actions are then applied in sequence, meaning later actions
are subject to the side effects of prior actions. It is the responsibility of each agent to confirm that it's previous actions had the desired effect.

Where actions occur during the same UTS the execution order chosen by the environment is also used during the visualisation.

