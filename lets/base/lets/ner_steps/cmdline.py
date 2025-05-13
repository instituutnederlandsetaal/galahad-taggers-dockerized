"""
Command line subprocess helper class.

"""

import subprocess
import logging
log = logging.getLogger(__name__)


class CommandLineHelper(object):
    """A helper class allowing arbitrary command line execution and retaining
       stdout, stderr and returncode.
    """

    def __init__(self, argument=None):
        self._tokens = argument
        self._out = None
        self._err = None
        self._returncode = None

    def get_all_tokens(self):
        """Returns a list of all command tokens accumulated so far."""
        return self._tokens

    def add_args(self, new_tokens, before=None):
        """Adds given list of command line arguments to the list of all arguments.
           If before is provided, will insert new arguments before that specified argument."""
        if before:
            index = self._tokens.index(before)
        else:
            index = len(self._tokens)

        for item in reversed(new_tokens):
            self._tokens.insert(index, item)

    def execute(self, timeout=None, shell=False): # /bin/sh
        """Executes the command and retains stdout, stderr and returncode."""
        if shell:
            tokens = " ".join(self._tokens)
        else:
            tokens = self._tokens
        log.debug("Executing %r", tokens)
        proc = subprocess.Popen(tokens, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        out, err = proc.communicate(timeout=timeout)
        self._out = out.decode('UTF-8')
        self._err = err.decode('UTF-8')
        self._returncode = proc.poll()

    def return_tokens(self):
        return self._tokens

    def returncode(self):
        return self._returncode

    def stdout(self):
        return self._out

    def stderr(self):
        return self._err
