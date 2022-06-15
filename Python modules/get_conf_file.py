from json import load as json_load
import get_catalogs_ways as gt
import xml.etree.cElementTree as ET
import os


def check_file(parent_path, folder, file_name):
    d = gt.get_catalogs_way(parent_path)
    check_f = os.path.exists(f"{d.get(folder)}\\{file_name}")
    if check_f is True:
        return True


def get_conf_file(path) -> dict:
    """
    Функция получает данные из файлов с настройками
    :param path: Путь к файлам
    :return:
    """
    dict_con_file = dict()
    w = gt.get_catalogs_way(path)
    # Получим файл настроек подключений

    for file in ['data_connect.json', 'questions_file.xml', 'start_work.xml', 'finish_work.xml']:
        name = file.split('.')[0]
        file_ext = file.split('.')[1]
        if check_file(path, name, file):

            if file_ext == 'json':
                read_file = open(f'{w.get(name)}\\{file}', "r")
                dict_con_file[name] = json_load(read_file)  # Получили настройки из файла
                read_file.close()  # Закрыли файл
            elif file_ext == 'xml':
                dict_con_file[name] = get_requests(f'{w.get(name)}\\{file}')
    return dict_con_file


def get_requests(way_to_file: dict) -> dict:
    """
    Функция получает и обрабатывает запрос из xml файла
    :param way_to_file: Путь к файлу с запросами
    :return:
    """
    tree = ET.ElementTree(file=f'{way_to_file}')
    fin_dic = dict()  # Конечный словарь
    tress = tree.getroot()  # Получим базовый элемент дерева
    for elem in range(len(list(tress))):
        time_dict = dict()
        time_dict[tress[elem].tag] = tress[elem].text

        for leaf in list(tress[elem]):
            time_dict[leaf.tag] = leaf.text

            if leaf.tag == 'columns_info' or leaf.tag == 'main_table':
                small_branch = list(leaf)

                # Итерация по типам столбцов
                second_time_dict = dict()
                for small_liaf in small_branch:
                    second_time_dict[small_liaf.tag] = small_liaf.text

                time_dict[leaf.tag] = second_time_dict  # добавим типы столбцов

        fin_dic[elem] = time_dict  # Объединим в конечный словарь
    return fin_dic

