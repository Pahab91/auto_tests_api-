import os
from dotenv import load_dotenv
'''Переменные окружения'''
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
config = {
    'LOGIN': os.environ.get('LOGIN'),
    'PASS': os.environ.get('PASS')

}
'''забираем логин и пароль из файла под названием .env , соответсвенно для корректной работы необходимо создать файл
 структура которого имееет вид:
LOGIN = ******
PASS = *******       
'''

