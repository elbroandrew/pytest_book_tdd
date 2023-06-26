import unittest
import unittest.mock
from multiprocessing.managers import SyncManager, ListProxy

'''
Класс Manager() модуля multiprocessing возвращает запущенный объект SyncManager, 
который можно использовать для совместного использования объектов между процессами.
'''


class TestChatAcceptance(unittest.TestCase):

    def test_message_exchange(self):
        with new_chat_server():
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
        client = ChatClient("User 1", connection_provider=unittest.mock.Mock())
        sent_message = client.send_message("Hello World")
        assert sent_message == "User 1: Hello World"

    def test_client_connection(self):
        connection_spy = unittest.mock.MagicMock()
        client = ChatClient("User 1", connection_provider=lambda *args: connection_spy)
        client.send_message("Hello World")
        connection_spy.broadcast.assert_called_with("User 1: Hello World")

    def test_client_fetch_messages(self):
        connection = unittest.mock.Mock()
        connection.get_messages.return_value = ["message1", "message2"]
        client = ChatClient("User 1", connection_provider=lambda *args: connection)
        starting_messages = client.fetch_messages()
        client.connection.get_messages().append("message3")
        new_messages = client.fetch_messages()

        assert starting_messages == ["message1", "message2"]
        assert new_messages == ["message3"]


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
        if self.last_command == 'dummy':
            return "#RETURN", None
        # handle other commands
        elif self.last_command == "create":
            return "#RETURN", ("fakeid", tuple())
        elif self.last_command == "append":
            self.messages.append(self.last_args[0])
            return "#RETURN", None
        elif self.last_command == "__getitem__":
            return "#RETURN", self.messages[self.last_args[0]]
        elif self.last_command in ("incref", "decref", "accept_connection"):
            return "#RETURN", None
        else:
            return "#ERROR", ValueError("%s - %r" % (self.last_command, self.last_args))

    def close(self):
        pass


class Connection(SyncManager):
    """
    The only thing we will have to do is register a single Connection.get_messages
    identifier in the manager. The purpose of that identifier will be to return the list of
    messages that are currently in the chat so that ChatClient can read them or append new
    messages
    """

    def __init__(self, address):
        self.register("get_messages", proxytype=ListProxy)
        super().__init__(address=address, authkey=b'mychatsecret')
        self.connect()

    """
    Then the Connection.broadcast method will be as simple as just getting the messages
    through Connection.get_messages and appending a new message to them
    """

    def broadcast(self, message):
        messages = self.get_messages()
        messages.append(message)


class ChatClient:

    def __init__(self, nickname, connection_provider=Connection):
        self._last_msg_idx = 0
        self.nickname = nickname
        self._connection = None
        self._connection_provider = connection_provider

    def send_message(self, message):
        sent_message = "{}: {}".format(self.nickname, message)
        self.connection.broadcast(sent_message)
        return sent_message

    def fetch_messages(self):
        messages = list(self.connection.get_messages())
        new_messages = messages[self._last_msg_idx:]
        self._last_msg_idx = len(messages)
        return new_messages

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._connection_provider(("localhost", 9090))
        return self._connection

    def _get_connection(self):
        c = Connection(("localhost", 9090))
        c.connect()
        return c


_messages = []


def _srv_get_messages():
    return _messages


class _ChatServerManager(SyncManager):
    pass


_ChatServerManager.register("get_messages", callable=_srv_get_messages, proxytype=ListProxy)


def new_chat_server():
    return _ChatServerManager(("", 9090), authkey=b'mychatsecret')


if __name__ == '__main__':
    unittest.main()
