import pytest
import requests
from requests.auth import HTTPBasicAuth
from settings import config

"""
Для запуска всех тестов автоматически необходимо ввести команду 'pytest test_api_ivi.py' в терминале.
Отчет сгенерирован с помощью модуля для пайтеста 'pip install pytest-html' файл отчета называется report.html 
его необходимо запускать через браузер.
Команда для генерации нового отчета 'pytest --html=report.html'
P.S. Проводил тестирование апи впервые в жизни, за один вечер, не искал готовых решений по общей структуре тестов
делал как мог, если бы перед глазами были готовые тесты по подобию которых можно сделать свои , то справился бы гораздо 
лучше и структура была бы в разы адекватнее.
"""


class TestGetCharacters:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.response = requests.get(
            'http://rest.test.ivi.ru/v2/characters',
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )
        self.character_keys = {'education', 'height', 'identity', 'name', 'other_aliases', 'universe', 'weight'}
        self.result_json = self.response.json()

    def test_code_is_200(self):
        # проверяем результат запроса
        assert self.response.status_code == 200, "статус код не 200"

    def test_type_json(self):
        # проверяем на json
        assert self.response.headers['Content-Type'] == "application/json", 'формат не json'

    def test_result_is_list(self):
        # проверяем что result это list
        assert isinstance(self.result_json.get('result'), list), "result не список"

    def test_dicts_in_result(self):
        # проверяем что в result находятся dict
        assert isinstance(self.result_json.get('result')[0], dict), "result не содержит словарь или пустой"

    def test_len_scheme(self):
        # проверяем на соответствие количества элементов в схеме
        self.dict_keys = set(self.result_json.get('result')[0].keys())
        assert len(self.dict_keys) == len(self.character_keys), 'не совпадает количество элементов'

    def test_scheme_structure(self):
        # сверяем структуры схемы с данными из задания
        self.dict_keys = set(self.result_json.get('result')[0].keys())
        assert self.dict_keys == self.character_keys, 'неправильная схема'


@pytest.mark.parametrize('name', ["Avalanche", "3-D+Man"])
# задаем параметризацию для того чтобы каждый тест в классе прогонялся сначала с именем из одного слова а потом с
# именем из двух слов
class TestGetHeroName:
    @pytest.fixture(autouse=True)
    def setup(self, name):
        self.response = requests.get(
            "http://rest.test.ivi.ru/v2/character?name={}".format(name),
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )
        self.result_json = self.response.json()
        self.character_keys = {'education', 'height', 'identity', 'name', 'other_aliases', 'universe', 'weight'}

    def test_name_code_is_200(self):
        # проверяем результат запроса
        assert self.response.status_code == 200, "status code is not 200"

    def test_name_type_json(self):
        # проверяем на json
        assert self.response.headers['Content-Type'] == "application/json", 'формат не json'

    def test_name_result_is_dict(self):
        # проверяем что result это dict
        assert isinstance(self.result_json.get('result'), dict), "result не словарь"

    def test_name_len_scheme(self):
        # проверяем на соответствие количества элементов в схеме
        self.dict_keys = set(self.result_json.get('result').keys())
        assert len(self.dict_keys) == len(self.character_keys), 'не совпадает количество элементов'

    def test_name_scheme_structure(self):
        # проверяем структуру схемы на соответствие данным из задания
        self.dict_keys = set(self.result_json.get('result').keys())
        assert self.dict_keys == self.character_keys, 'неправильная схема'


class TestPostCharacters:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = "http://rest.test.ivi.ru/v2/character"
        self.hero = {"name": "snake", "universe": "Marvel Universe",
                     "education": "High school (unfinished)", "weight": 104,
                     "height": 1.90, "identity": "Publicly known"}
        self.response = requests.post(
            self.url, json=self.hero,
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )
        self.result_json = self.response.json()
        # создаем финализатор который будет удалять созданный пост после прохождения тестов
        yield self.result_json
        self.response = requests.delete(
            'http://rest.test.ivi.ru/v2/character?name=' + self.result_json.get("result").get('name'),
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )

    def test_post_type_json(self):
        # проверяем на json
        assert self.response.headers['Content-Type'] == "application/json", 'формат не json'

    def test_post_code_is_200(self):
        # проверяем результат запроса
        assert self.response.status_code == 200, "статус код не 200"

    def test_post_result_is_dict(self):
        # проверяем что result это dict
        assert isinstance(self.result_json.get('result'), dict), "result не словарь"

    def test_post_name_in_result_is_str(self):
        # проверяем что значения ключа name это str
        assert isinstance(self.result_json.get('result').get('name'), str), "значение ключа name не str"

    def test_post_weight_in_result_is_float(self):
        # проверяем что значения ключа weight это float
        assert isinstance(self.result_json.get('result').get('weight'), float), "значение ключа weight не float"


class TestDeleteCharacters:
    def test_delete(self):
        # для начала создадим героя через пост
        self.url = "http://rest.test.ivi.ru/v2/character"
        self.hero = {"name": "supermUn", "universe": "Marvel Universe",
                     "education": "High school (unfinished)", "weight": 104,
                     "height": 1.90, "identity": "Publicly known"}
        self.response = requests.post(
            self.url, json=self.hero,
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )

        self.result_json = self.response.json()
        self.char_name = self.result_json.get("result").get('name')
        # удаляем персонажа посредством метода delete
        self.response = requests.delete(
            'http://rest.test.ivi.ru/v2/character?name=' + self.char_name,
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )
        # проверяем ссобщение удалилось ли имя
        assert self.char_name and 'is deleted' in str(self.response.json()), "имя не удалилось"

    def test_delete_with_no_name_in_db(self):
        self.name = "supermUn"
        # проверка на отсуствие имени в DB
        self.response = requests.delete(
            'http://rest.test.ivi.ru/v2/character?name=' + self.name,
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )
        assert "No such name" in str(self.response.json()), "имя содержится в базе данных"


class TestPutCharacters:
    # фикстура для однократного запуска функции при тестировании всего класса
    @pytest.fixture(scope='function')
    def setup(self):
        # создаем нового героя для будущей перезаписи
        self.url = "http://rest.test.ivi.ru/v2/character"
        self.hero = {"name": "Hawkeye", "universe": "Marvel Universe",
                     "education": "High school (unfinished)", "weight": 104,
                     "height": 1.90, "identity": "Publicly known"}
        self.response = requests.post(
            self.url, json=self.hero,
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )
        self.result_json = self.response.json()

    def test_put_character(self):
        # перезаписываем созданного в прошлом героя
        self.url = "http://rest.test.ivi.ru/v2/character"
        self.hero = {"name": "Hawkeye", "universe": "Marvel Universe",
                     "education": "High school (unfinished)", "weight": 105,
                     "height": 1.90, "identity": "Publicly known"}
        self.response = requests.put(
            self.url, json=self.hero,
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )
        self.result_json = self.response.json()
        assert self.result_json.get('result').get('weight') == 105, 'данные не перезаписались'

    def test_put_character2(self):
        # перезаписываем созданного в прошлом героя
        self.url = "http://rest.test.ivi.ru/v2/character"
        self.hero = {"name": "Hawkeye", "universe": "Marvel Universe",
                     "education": "High school (unfinished)", "weight": 60,
                     "height": 1.50, "identity": "Publicly known"}
        self.response = requests.put(
            self.url, json=self.hero,
            # авторизация посредством логина и пароля из отдельного файла
            auth=HTTPBasicAuth(config.get('LOGIN'), config.get('PASS'))
        )
        # проверяем перезаписались ли данные
        self.result_json = self.response.json()
        assert self.result_json.get('result').get('universe') == "Marvel Universe", 'данные не перезаписались'
