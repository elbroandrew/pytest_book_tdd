import unittest

from auth.auth import Authentication, Authorization



"""
So TestAuthentication.test_login will be a unit test that verifies the behavior of the
Authentication.login unit, while TestAuthorization.test_can will be a unit test
that verifies the behavior of the Authorization.can unit
"""


class TestAuthentication(unittest.TestCase):
    def test_login(self):
        auth = Authentication()
        auth.USERS = [{"username": "testuser",
                       "password": "testpass"}]

        resp = auth.login("testuser", "testpass")

        assert resp == {"username": "testuser",
                        "password": "testpass"}


class TestAuthorization(unittest.TestCase):
    def test_can(self):
        authz = Authorization()
        authz.PERMISSIONS = [{"user": "testuser",
                              "permissions": {"create"}}]
        resp = authz.can({"username": "testuser"}, "create")
        assert resp is True


"""
Here, we have the notable difference that TestAuthentication.test_login is a SOCIABLE
unit test as it depends on Authentication.fetch_user while testing
Authentication.login, and TestAuthorization.test_can is instead a SOLITARY unit
test as it doesn't depend on any other unit.
"""


# Integration test:

class TestAuthorizeAuthenticatedUser(unittest.TestCase):
    def test_auth(self):
        auth = Authentication()
        authz = Authorization()

        auth.USERS = [{"username": "testuser",
                       "password": "testpass"}]

        authz.PERMISSIONS = [{"user": "testuser",
                              "permissions": {"create"}}]
        u = auth.login("testuser", "testpass")
        resp = authz.can(u, "create")
        assert resp is True


if __name__ == '__main__':
    unittest.main()
