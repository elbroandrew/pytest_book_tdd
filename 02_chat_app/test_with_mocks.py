import unittest
from unittest.mock import Mock

"""
mock - это пустой объект, которому так же можно создать методы и тд.
"""


# ф-ия, которую необходимо протестить
def read_file(f):
    print("\nREADING THE FILE")
    return f.read()


class TestReadFile(unittest.TestCase):

    def test_read_file(self):
        m = Mock()
        m.read.return_value = "Hello World"
        print(read_file(m))






