try:
    from . import agent
    from . import actEnum
except:
    import agent
    import actEnum

Agent = agent.Agent
Act = actEnum.Act
DumbMind = agent.DumbMind
ActEnum = actEnum.ActEnum
