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
        print(read_file(m))
        print(m.read.call_count)  # 1
        m.read.assert_called_with()  # f.read was called with no args.







