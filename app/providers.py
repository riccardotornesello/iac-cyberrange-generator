from . import environment


class Azure():
    def __init__(self, options: dict):
        for k, v in options.items():
            environment.add_var(k, v)
