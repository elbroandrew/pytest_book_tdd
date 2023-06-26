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

    def test_client_connection(self):
        client = ChatClient("User 1")

        connection_spy = unittest.mock.MagicMock()
        with unittest.mock.patch.object(client, "_get_connection", return_value=connection_spy):
            client.send_message("Hello World")
        # assert that the spy was called with the expected data to broadcast
        connection_spy.broadcast.assert_called_with(("User 1: Hello World"))


class TestConnection(unittest.TestCase):
    def test_broadcast(self):
        """
        unittest.mock.patch.object is a convenience method that allows us to replace a
        method or attribute of an object with a unittest.mock.Mock for the whole duration of the
        code block within the context. So in this case, we disabled the Connection.connect
        method so that the connection could be created without a server
        """
        with unittest.mock.patch.object(Connection, "connect"):
            c = Connection(("localhost", 9090))

        with unittest.mock.patch.object(c, "get_messages", return_value=[]):
            c.broadcast("some message")
            assert c.get_messages()[-1] == "some message"

    def test_exchange_with_server(self):
        with unittest.mock.patch(  # patch replaces standard impl of the server/client channel (pickle) with ours.
            "multiprocessing.managers.listener_client",
            new={"pickle": (None, FakeServer())}
        ):
            c1 = Connection(("localhost", 9090))
            c2 = Connection(("localhost", 9090))

            c1.broadcast("connected message")
            assert c2.get_messages()[-1] == "connected message"


class FakeServer:
    def __init__(self):
        self.last_command = None
        self.last_args = None
        self.messages = []

    def __call__(self, *args, **kwargs):
        # make the SyncManager think that a new connection was created.
        return self

    def send(self, data):
        # track any command that was sent to the server
        callid, command, args, kwargs = data
        self.last_command = command
        self.last_args = args

    def recv(self, *args, **kwargs):
        # for now we don't support any command, so our fake server responds with error to any command.
        return "#ERROR", ValueError("%s - %r" % (self.last_command, self.last_args))


class ChatClient:

    def __init__(self, nickname):
        self.nickname = nickname
        self._connection = None

    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(sent_message)
        return sent_message

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._get_connection()
        return self._connection

    @connection.setter
    def connection(self, value):
        if self._connection is not None:
            self._connection.close()
        self._connection = value

    def _get_connection(self):
        return Connection(("localhost", 9090))


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
