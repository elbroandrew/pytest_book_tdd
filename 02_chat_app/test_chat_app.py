import unittest
import unittest.mock
from multiprocessing.managers import SyncManager


class TestChatAcceptance(unittest.TestCase):

    def test_message_exchange(self):
        user1 = ChatClient("John Doe")
        user2 = ChatClient("Harry Potter")

        user1.send_message("Hello World")
        messages = user2.fetch_messages()
        assert messages == ["John Doe: Hello World"]


class TestChatClient(unittest.TestCase):
    def test_nickname(self):
        client = ChatClient("User 1")
        assert client.nickname == "User 1"

    def test_send_message(self):
        client = ChatClient("User 1")
        client.connection = unittest.mock.Mock()
        sent_message = client.send_message("Hello World")
        assert sent_message == "User 1: Hello World"


class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        c = Connection(("localhost", 9090))
        c.broadcast("some message")
        assert c.get_messages()[-1] == "some message"


class ChatClient:

    def __init__(self, nickname):
        self.nickname = nickname

    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(message)
        return sent_message


"""
A possible idea for how to implement cross-client communication is to use a
multiprocessing.managers.SyncManager and store the messages in a list that is
accessible by all the clients that connect to it.
"""
class Connection(SyncManager):
    """
    The only thing we will have to do is register a single Connection.get_messages
    identifier in the manager. The purpose of that identifier will be to return the list of
    messages that are currently in the chat so that ChatClient can read them or append new
    messages
    """
    def __init__(self, address):

        self.register("get_messages")
        super().__init__(address=address, authkey=b'mychatsecret')
        self.connect()
    """
    Then the Connection.broadcast method will be as simple as just getting the messages
    through Connection.get_messages and appending a new message to them
    """
    def broadcast(self, message):
        messages = self.get_messages()
        messages.append(message)


if __name__ == '__main__':
    unittest.main()
