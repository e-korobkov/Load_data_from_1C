import os
from json import load as json_load
import xml.etree.cElementTree as ET
from pathlib import Path


def get_catalogs_way(parent_path) -> dict:
    w = dict()  # Словарь для хранения путей
    w['way_to_py'] = str(parent_path.parent)  # Получим путь к каталогу
    time_str = str(parent_path.parent.parent)

    # Путь к каталогу БД
    w['way_to_bd'] = time_str + '\\Postrge_BD'

    # Путь к каталогу конфигурационных файлов
    w['questions_file'] = time_str + '\\Сonfiguration_files'
    w['data_connect'] = time_str + '\\Сonfiguration_files'
    w['start_work'] = time_str + '\\Сonfiguration_files'
    w['finish_work'] = time_str + '\\Сonfiguration_files'
    w['data_file'] = time_str + '\\Data_files'

    # Путь к каталогу хранения Pickle данных
    w['way_to_pickle'] = time_str + '\\Pickle_data'
    w['way_to_pickle_after_change'] = time_str + '\\Pickle_data_after_change'
    w['pickle_ml_model'] = time_str + '\\Pickle_ML_model'

    # Путь к файлу логов
    w['log_file'] = time_str + '\\Log_file'

    return w


# Функция чтения файлов настройки подключения
def get_conf_file(path) -> (dict, dict, dict, dict):
    ways = get_catalogs_way(path)

    # Получим файл настроек подключений
    try:
        read_file = open(f'{ways.get("data_connect")}\\data_connect.json', "r")
        dict_connect = json_load(read_file)  # Получили настройки из файла
        read_file.close()  # Закрыли файл
    except:
        dict_connect = None
    
    # Фолучим файл с запросами
    try:
        dict_request = parse_json(
            f'{ways.get("conf_file_question")}\\questions_file.xml')
    except:
        dict_request = None

    # Фолучим файл начального выполнения
    try:
        dict_start = parse_json(f'{ways.get("start_work")}\\start_work.xml')
    except:
        dict_start = None

    # Получим файл финального выполнения
    try:
        dict_finish = parse_json(f'{ways.get("finish_work")}\\finish_work.xml')
    except:
        dict_finish = None

    return (dict_connect, dict_request, dict_start, dict_finish)


# Функция получения данных из файла запроссов
def parse_json(way_to_file: dict) -> dict:
    tree = ET.ElementTree(file=f'{way_to_file}')
    fin_dic = dict()  # Конечный словарь
    tress = tree.getroot()  # Получим базовый элемент дерева
    for elem in range(len(list(tress))):
        time_dict = dict()
        time_dict[tress[elem].tag] = tress[elem].text

        for leaf in list(tress[elem]):
            time_dict[leaf.tag] = leaf.text

            if leaf.tag == 'columns_info':
                small_branch = list(leaf)

                # Итерация по типам столбцов
                second_time_dict = dict()
                for small_liaf in small_branch:
                    second_time_dict[small_liaf.tag] = small_liaf.text

        time_dict['columns_info'] = second_time_dict  # добавим типы столбцов

        fin_dic[elem] = time_dict  # Объединим в конечный словарь
    return fin_dic


if __name__ == '__main__':
    path = Path(os.path.realpath('__file__'))
    rez = get_conf_file(path)
