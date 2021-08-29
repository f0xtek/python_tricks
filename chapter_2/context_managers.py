# You can use the 'with' statement to some common resource management
# patterns by abstracting functionality allowing them to be factored out
# and reused.
#
# example, when opening files, using a context manager via the 'with' statement
# Python will ensure that f.close() is automatically called for you to release the file
# handle.
with open('test.txt', 'w') as f:
    f.write('Hello, World!')

# The equivalent code without a context manager would be
f = open('test.txt', 'w')
try:
    f.write('Hello, World!')
finally:
    f.close()

# It would be important to run this in try/finally to make sure the file
# is closed, even if an exception is raised when writing.
#
# You can implement context managers in your own objects allowing you to use the
# with statement on your custom objects, by implementing the __enter__ and __exit__
# methods on your class.
#
# Example
class ManagedFile:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.file = open(self.name, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()


with ManagedFile('test.txt') as f:
    f.write('Hello, World!')
    f.write('end of file')

# The contextlib module also provides more functionality on top of conetxt managers
# if your use case matches what is offered by contextlib
from contextlib import contextmanager

@contextmanager
def managed_file(name):
    """
    A generator-based factory function to create
    a managed file. Functionally equivalent to the
    class-based implementation.
    :param name: The filename
    """
    try:
        f = open(name, 'w')
        yield f
    finally:
        f.close()


with managed_file('test.txt') as f:
    f.write('Hello, World!')


# Example, a text indenter in a report generating program
class Indenter:
    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print(self, msg):
        print(' ' * self.level + msg)


with Indenter() as indent:
    indent.print('Hi')
    with indent:
        indent.print('hello')
        with indent:
            indent.print('bonjour')
    indent.print('hey')


# Example: a timer context-manager
from datetime import datetime
import time


class Timer:
    def __init__(self):
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = datetime.utcnow()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.utcnow()
        print(f'Function duration:  {self.end - self.start}')


with Timer() as timer:
    print('Starting...')
    time.sleep(5)
    print('end.')

