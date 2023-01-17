import unittest


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


class ChatClient:

    def __init__(self, nickname):
        self.nickname = nickname


if __name__ == '__main__':
    unittest.main()
