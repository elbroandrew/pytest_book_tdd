To run this simple console app just enter:

`python -m todo`

Короче, я так понимаю суть такова с тредами: запускаю приложение 
и отдельно тесты в другом треде. Т.е. тесты в работе, а приложение можем запустить/остановить
(т.е. в новом треде стартануть его).

To run `unit tests`:

Go into `cd 03_Todo_list_TDD` dir

then do `python -m unittest discover -k unit`

`-k` option only runs the tests that contain the provided substring,
in our case it is `unit` substring and will run tests from this dir.
It also can run tests with `unit` in the test name.