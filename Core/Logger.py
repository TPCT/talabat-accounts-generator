from time import strftime
from textwrap import fill
import colorama
from os import makedirs, path
from sys import stdout
import termcolor
from threading import Lock


class Logger:
    DEFAULT_FOLDER = "logs"

    def __init__(self, width=500, debug=False):
        self.lock = Lock()
        self.width = width
        colorama.init()
        self._debug = debug
        self._output = None

    def error(self, message):
        message = f"[ERROR {strftime('%Y-%m-%d %H:%M:%S')}] {str(message).lower()}"
        self._log(termcolor.colored(message, 'red'))

    def warn(self, message):
        message = f"[WARNING {strftime('%Y-%m-%d %H:%M:%S')}] {str(message).lower()}"
        self._log(termcolor.colored(message, 'white'))

    def log(self, message):
        message = f"[NORMAL {strftime('%Y-%m-%d %H:%M:%S')}] {str(message).lower()}"
        self._log(termcolor.colored(message, 'yellow'))

    def _log(self, message):
        makedirs(Logger.DEFAULT_FOLDER, exist_ok=True)
        log_file = path.join(Logger.DEFAULT_FOLDER, f"log-{strftime('%Y-%m-%d')}.txt") if not self._debug else stdout
        with self.lock:
            self._output = open(log_file if self._debug else log_file,
                                'w+' if not path.exists(log_file) else 'a+') \
                if not self._debug else stdout
            print(fill(message,
                       self.width, subsequent_indent="\t",
                       replace_whitespace=False),
                  file=self._output)
