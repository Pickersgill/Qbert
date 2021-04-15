try:
    from . import environment
except:
    import environment

Environment = environment.Environment
Env = Environment
