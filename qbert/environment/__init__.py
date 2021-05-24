try:
    from . import environment
    from . import env_utils
except:
    import environment
    import env_utils

ENTRANCE_SIZE = environment.ENTRANCE_SIZE
Environment = environment.Environment
Env = Environment
