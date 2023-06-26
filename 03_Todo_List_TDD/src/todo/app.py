import functools

class TodoApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):  # use builtin input and print to input and output
        self._in, self._out = io
        self._quit = False
        self._entries = []

    def run(self):
        self._quit = False
        while not self._quit:
            self._out(self.prompt(""))
            command = self._in()
            self._dispatch(command)
        self._out("bye!\n")

    def prompt(self, output):
        return """TODOs:
{}

> """.format(output)

    def _dispatch(self, cmd):
        cmd, *args = cmd.split(" ", 1)
        executor = getattr(self, "cmd_{}".format(cmd), None)
        if executor is None:
            self._out("Invalid command: {}\n".format(cmd))
            return
        executor(*args)

    def cmd_add(self, what):
        self._entries.append(what)
