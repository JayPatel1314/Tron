from typing import Callable

import pyrogram
from pyrogram.filters import Filter
from pyrogram.scaffold import Scaffold

from tronx.variable import CMD_HELP



class OnMessage(Scaffold):
    def on_msg(
        self = None,
        filters = None,
        plug: str = "",
        cmd: str = "",
        usage: str = "",
        group: int = 0
    ) -> callable:
        """Decorator for handling messages.

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.MessageHandler`.

        Parameters:
            filters (:obj:`~pyrogram.filters`, *optional*):
                Pass one or more filters to allow only a subset of messages to be passed
                in your function.

            info (dict, *optional)
                command name and information about this command.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        CMD_HELP.update({plug: {cmd: usage}})

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(pyrogram.handlers.MessageHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.MessageHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
