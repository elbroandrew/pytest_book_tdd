Book: `"Crafting test-driven software with python -- A.Molina"`

- If folders' structure looks like this:

`working_dir/auth.py`

`working_dir/test_auth.py`

Then run single test Win10 :

`python <test file name>.py <test name> <another test name>`

examples:

`python test_auth.py TestAuthentication` or

`python test_auth.py TestAuthentication TestAuthorization`

- if folders' structure looks like this:

`working_dir/auth_package/__init__.py`

`working_dir/auth_package/auth.py`

`working_dir/tests<directory>/test_auth.py`

then run all tests from cmd win10:

`python -m unittest tests/test_auth.py`
