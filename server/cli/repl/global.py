import click

_global_commands = {}


class GlobalCommand(click.Command):
    def __init__(self):
        pass

# def register_global_command(names, target, description=None):
#     if not hasattr(target, "__call__"):
#         raise ValueError("Internal command must be a callable")
#
#     if isinstance(names, str):
#         names = [names]
#
#     elif isinstance(names, Mapping) or not isinstance(names, Iterable):
#         raise ValueError(
#             '"names" must be a string, or an iterable object, but got "{}"'.format(
#                 type(names).__name__
#             )
#         )
#
#     for name in names:
#         _global_commands[name] = (target, description)
