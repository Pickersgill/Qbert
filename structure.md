
## The Problem

What's going on? The scenario:

    + N agents want to complete their tasks.
    + Each task can only be completed by a kiosk.
    + Each kiosk has a finite number of servers and takes a set time to complete a service
    + How long do the agents take to complete their tasks on average? As a whole? Minimum?

The naive approach is for each agent to visit the kiosk for it's task in sequence. How good is the
naive approach? Does it perform better than different strategies which use greater information:

    + If the agents know the time of each kiosk, they could perform there tasks in order of time
        taken or vise versa.

    + If the agents know what each other agents tasks are, they can make some kind of informed decision 
        based on how many agents have to visit each kiosk. Does this work better or worse than the naive
        approach.

## The Solution

Let's build a little world (environment) for our agents. In the environment they can move around in 2d space
and visit kiosks. When they visit a kiosk they join the queue for that kiosk. The agents are each represented
by a mind. The mind will tell the environment what each agent should do at each UTS (Unit Time Step). 
It is possible for one mind to command many agents, and so it may be better to model this problem with a 
Mind object which accepts as a visitor the agent object for whom it is deciding an action.

### The Environment:

+ The environment contains all the agents' physical positions.
 
+ It wraps a data structure containing each agent
  object.
 
+ Agents are free to move in 2d space within a bounded plane.
 
+ The kiosks exist at the edges of plane.
 
+ When an agents enters a Kiosk it is added to the queue for that kiosk.

+ The agent leaves the the kiosk when it is served.

+ During each UTS the environment will ask the agents what they want to do and enact their action.

+ Agent actions are decided sequentialy. The decisions of the first agent in the queue may affect the
    decision of a later agent.

+ The environment should be capable of running headless and produce some kind of record for data analysis.

+ This record could be a list of events which can be interpreted later.

+ The constructor for the environment should accept arguments for:

    - The number of agents with each mind type.

    - The size of the environment.

    - Some description of the kiosks. (Possibly a list of kiosk objects).

### The Agents:

+ Each agent probably has a colour identifying it. This helps when there are many minds acting in the
    same environment

+ The agents themselves are really just a collection of attributes describing the agents position, queueing
    status, task list etc.

+ The agent will be assigned a mind at birth (dystopian!). It will ask the mind what it should do when
    appropriate.

### The Minds:

+ The minds must all look the same, they are an interface. The mind doesn't store any data about agents. 
    It is a collection of functions which will decide how an agent should behave.

+ The available actions should be predefined. Really the only thing the agent needs to decide is which queue
    to "target" but a health set of actions would be: ["run", "walk", "face", "queue"]

### The Kiosks:

+ A kiosk is basically a queue wrapper.

+ It needs to store how many agents are queueing.

+ How many servers there are.

+ How long (UTS) does a server take.

+ What service is it providing?

