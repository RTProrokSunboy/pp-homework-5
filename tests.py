import os
from decorators import logger_func, logger
from old_project_function import create_bar_and_find_tegs, get_requests, \
    get_parametres


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(a=2, b=2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(a=6, b=2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(a=4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_func(path)
        def hello_world():
            return 'Hello World'

        @logger_func(path)
        def summator(a, b=0):
            return a + b

        @logger_func(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


@logger
def test_3():
    url = 'https://spb.hh.ru/search/vacancy'
    end_page = True
    count_page = 0
    while end_page:
        div, soup = get_requests(url, get_parametres(count_page), id="a11y-main-content")
        serp_items = div.find_all(class_="serp-item")
        end_page = soup.find(attrs={"data-qa": "pager-next"})
        if end_page:
            print('Страница: ', count_page + 1)
        else:
            print('Последний лист')
            print('Страница: ', count_page + 1)
            end_page = False

        create_bar_and_find_tegs(serp_items)

        print('-' * 80)
        count_page += 1
