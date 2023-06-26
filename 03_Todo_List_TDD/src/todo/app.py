import functools

class TodoApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):  # use builtin input and print to input and output
        self._in, self._out = io
        self._quit = False

    def run(self):
        self._quit = False
        while not self._quit:
            self._out(self.prompt(""))
            command = self._in()
        self._out("bye!\n")

    def prompt(self, output):
        return """TODOs:
{}

> """.format(output)

