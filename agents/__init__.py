try:
    from . import agent
    from . import actEnum
except:
    import agent
    import actEnum

Agent = agent.Agent
ActEnum = actEnum.ActEnum
