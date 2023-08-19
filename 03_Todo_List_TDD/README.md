To run this simple console app just enter:

если ошибка NoModuleNamed todo:

иду в `src`, где лежит `setup.py`, запускаю команду `pip install .`

или `pip install -e .` (сбилдит проект, и смогу использовать изменеия без переустановки todo приложения типа того)

затем только иду назад в папку `03_Todo_List_TDD`

и запускаю тесты:

`python -m unittest discover -k unit`

---

`python -m todo` -> запускает приложение (т.к. есть `__main__` в `src`)

Короче, я так понимаю суть такова с тредами: запускаю приложение 
и отдельно тесты в другом треде. Т.е. тесты в работе, а приложение можем запустить/остановить
(т.е. в новом треде стартануть его).

To run `unit tests`:

Go into `cd 03_Todo_list_TDD` dir

then do `python -m unittest discover -k unit`

`-k` option only runs the tests that contain the provided substring,
in our case it is `unit` substring and will run tests from this dir.
It also can run tests with `unit` in the test name.