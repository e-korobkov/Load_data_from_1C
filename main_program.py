import sys
from pathlib import Path
import pythoncom
import win32com.client
import pandas as pd
import datetime
import os
import xml.etree.cElementTree as ET
import re
from apscheduler.schedulers.background import BackgroundScheduler
import time
from multiprocessing import Pool

my_modules_way = '\\'.join(str(e) for e in os.path.realpath(__file__).split('\\')[:2]) + '\\Python modules\\'
sys.path.insert(0, my_modules_way)
import get_conf_file as gcf
import work_with_pickle_data as spd
import work_with_postgres as wwp
import work_with_log_file as lg_file


def connect_1c(dict_connect: dict) -> win32com:
    """
    Функция подключается к серверу 1С.

    :param dict_connect: Данные для подключения к 1С
    :return: COM объект подключения к серверу 1С
    """
    srv = dict_connect.get('data_connect').get('1c').get("Srv")
    ref = dict_connect.get('data_connect').get('1c').get("Ref")
    usr = dict_connect.get('data_connect').get('1c').get("login")
    pwd = dict_connect.get('data_connect').get('1c').get("password")
    # Подключимся к 1С
    v83_conn_string = f'Srvr={srv};Ref={ref};Usr="{usr}";Pwd={pwd};'
    pythoncom.CoInitialize()
    v83 = win32com.client.Dispatch("v83.COMConnector").Connect(v83_conn_string)
    return v83


def make_df(req: dict) -> pd.DataFrame:
    # Базовый DataFrame как таблица
    base_df = pd.DataFrame(data=None, columns=list(req.keys()))
    return base_df


def query_to_1c(com_object: win32com, request_to_1c: str, columns_info: dict) -> object:
    """
    Функция выполняет запрос к серверу 1С на "языке запросов 1С".
    
    :param com_object: COM объект подключения к 1С
    :param request_to_1c: Текст запросса на "языке запросов 1С"
    :param columns_info: Имена столбцов, они-же пресдонимы столбцов из текста запроса. 
    :return: Результат запроса в DataFrame, COM объект подключения к 1С
    """

    # Выполним запрос
    query = com_object.NewObject("Query", request_to_1c)
    # Результат запроса - Итератор
    query_result_iterator = query.Execute().Choose()
    # Создаем time_df для записи в него данных из 1С
    time_df = make_df(columns_info)
    while query_result_iterator.Next():
        time_dict = dict()
        for elem in time_df:
            time_dict[elem] = getattr(query_result_iterator, elem)
        # Создаем DF с с одной записью
        single_df = pd.DataFrame.from_dict([time_dict])
        # Склеим df
        time_df = pd.concat([single_df, time_df], ignore_index=True)
    return time_df, com_object


def get_requests(way_to_file: dict) -> dict:
    """Функция получения данных из файла запроссов"""
    tree = ET.ElementTree(file=f'{way_to_file}')
    fin_dic = dict() # Конечный словарь
    tress = tree.getroot() # Получим базовый элемент дерева
    for elem in range(len(list(tress))):
        time_d = dict()
        time_d[tress[elem].tag] = tress[elem].text
        for leaf in list(tress[elem]):
            time_d[leaf.tag] = leaf.text
            if leaf.tag == 'columns_info':
                small_branch = list(leaf)
                # Итерация по типам столбцов
                second_time_d = dict()
                for small_leaf in small_branch:
                    second_time_d[small_leaf.tag] = small_leaf.text
        time_d['columns_info'] = second_time_d  # добавим типы столбцов
        fin_dic[elem] = time_d  # Объединим в конечный словарь
    return fin_dic


def change_request(date: datetime.date, q: str) -> str:
    """
    Функция изменяет текст запроса к 1С - вставляет дату (как нижную границу запроса)
    :param date: Дата
    :param q: Исходный текст запроса.
    :return: Текст запроса к 1С.
    """
    span = re.search(r'ЗАМЕНИТЬДАТУ', q)
    while span:
        span = re.search(r'ЗАМЕНИТЬДАТУ', q)
        if span is not None:
            # Создадим нужную дату
            # Всегда беру данные на начало дня (старая реализация, не вижу смысла переделывать)
            between = f'ДАТАВРЕМЯ({date.year}, {date.month}, {date.day}, 0, 0, 0)'
            # Вставим в запрос новую дату
            q = q[:span.start()] + between + q[span.end():]
    return q


def change_data_type_after_1c(columns: dict, df: pd.DataFrame) -> pd.DataFrame:
    """
    Данные из 1С прилетают строковые.
    Данная функция изменяем str на нужный.

    :param columns: Данные о типах данных
    :param df: Таблица с данными из 1С
    :return: Таблица с данными из 1С
    """
    for col in columns.keys():
        df[col].replace({'None': None}, inplace=True)
        # Тип float
        if columns.get(col) == 'numeric' or columns.get(col) == 'bigserial':
            for number, series in df.iterrows():
                # Удаляем пробел
                df.at[number, col] = str(series[col]).replace('\xa0', '')
                # Заменяем ',' на '.'
                if type(df.at[number, col]) == str and ',' in df.at[number, col]:
                    time_list = df.at[number, col].split(',')
                    df.at[number, col] = float(f'{time_list[0]}.{time_list[1]}')
                else:
                    if df.loc[number, col] != 'None':
                        df.at[number, col] = float(df.at[number, col])
            df[col].replace({'None': None}, inplace=True)
            df[col] = pd.to_numeric(df[col])
        # Тип Дата
        elif columns.get(col) == 'date':
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='ignore')
            # Заменим NaT на None
            df[col] = df[col].astype(object).where(df[col].notnull(), None)
        # Отсутствующие данные заменим на None
        elif columns.get(col) == 'text':
            if '' in df[col].unique():
                df[col].replace({'': None}, inplace=True)
    df = df.where(pd.notnull(df), None)
    return df


def date_calculation(delta: int) -> datetime.date:
    """
    Функция на основании указанной дельты расчитывает границу первой загрузки

    :param delta: Кол-во шагов назад в днях
    :return: Начальная дата загрузки
    """
    delta = datetime.timedelta(days=int(delta))
    previously_data = datetime.datetime.now() - delta
    # Для отработки предшествующих нулей
    time_list = [0, 0, 0]
    time_list[0] = str(previously_data.year)
    time_list[1] = str(previously_data.month)
    time_list[2] = str(previously_data.day)
    for number in range(len(time_list)):
        if len(time_list[number]) == 1:
            time_list[number] = f'0{time_list[number]}'
    previously_data = datetime.date.fromisoformat(
        f'{time_list[0]}-{time_list[1]}-{time_list[2]}')
    return previously_data


def req_definition(dict_req: dict, dict_connect: dict, req: dict.keys) -> (str, datetime.date):
    """
    Функция изминяет текст запросса к 1С.

    :param dict_req: Блок с данными по запросу + текст запросса к 1С.
    :param dict_connect: Данные для подключения к базе данных.
    :param req: Признак обрабатываемого блока с запросом.
    :return : Текст запросса к 1С, дата последнего запросса.
    """

    # Если тип "documents", то нужно получить дату последнего обновления
    # Если это первая загрузка, то кол-во загружаемых дней получим из файла настроек
    # Если уже были загрузки, то границу загрузки установим по последней.
    if dict_req[req]['tables_type'] == 'documents':
        con = wwp.connect_postgre(dict_connect, 'main_base')
        # Вычислим дату последнего "обновления"
        status_df, con = wwp.work_with_data(**{"type": "get", "con": con, "select": '*',
                                               "from": "last_download", "condition":
                                                   {"table_name": {dict_req[req].get('databases_tables'): "="}}})
        con.close()

        if status_df.empty: # Первая загрузка
            req_date = date_calculation(dict_req[req]['relevance_time'])
            req_to_1c = change_request(req_date, dict_req[req]['text_request'])
        else:  # Были загрузки
            req_date = status_df.loc[0, 'last_update']
            req_to_1c = change_request(req_date, dict_req[req]['text_request'])
        return req_to_1c, req_date

    # Данные типа "directories"(справочник), не имеют поля date (т.е. нет признака "дата последнего изменения")
    # поэтому перегружаются полностью
    elif dict_req[req]['tables_type'] == 'directories':
        req_to_1c = dict_req[req]['text_request']
        # Дату вернем как None
        return req_to_1c, None


def work_with_postgre(all_dt_dict: dict, dict_connect: dict):
    """
    Функция записи новых данных в БД

    :param all_dt_dict: Данные полученные из 1С (по всем запроссам), соединенные в одном словаре.
    :param dict_connect: Данные для подключения к базе данных.
    :return : None
    """
    con = wwp.connect_postgre(dict_connect, 'main_base')
    for sql_table in all_dt_dict.keys():  # Итерация по таблицам с данными
        cur = con.cursor()
        column = all_dt_dict.get(sql_table)[1]
        # Блок исключения даных с временным ключем.
        # "guid" может быть равен "00000000-0000-0000-0000-000000000000", такое возможно, если данные получены
        # в промежутке после создания "объекта в 1С" и запуском "регламентного задания 1С - обновления guid"
        if column == 'guid':
            time_df = all_dt_dict.get(sql_table)[2]
            all_dt_dict.get(sql_table)[2] = time_df.loc[time_df['guid'] != "00000000-0000-0000-0000-000000000000"]

        # Проверка на пустой результат запросса из 1С (это не ошибка- к примеру справочник без данных)
        if all_dt_dict.get(sql_table)[2].empty is True:
            continue

        # Удаление старых данных
        if all_dt_dict.get(sql_table)[0] == 'documents':
            # Установим правило сравнения для функции удаления
            rules = "="  # Остальные столбцы типа guid, условие удаления всегда "="
            del_series = all_dt_dict.get(sql_table)[2][column].unique()
            # для обработки столбца типа date условие удаления всегда ">="
            if all_dt_dict.get(sql_table)[5] == "date":
                rules = ">="
                del_series = [str(min(all_dt_dict.get(sql_table)[2][column].unique()))]

            for delete_key in del_series:
                cur = wwp.cur = wwp.work_with_data(**{"type": "del", "cur": cur, "delete": sql_table, "condition": {
                    column: {delete_key: rules}}})
        else:
            cur = wwp.cur = wwp.work_with_data(**{"type": "del", "cur": cur, "delete": sql_table})
        # Добавление новых данных
        cur = wwp.execute_many(cur, all_dt_dict.get(sql_table)[2], sql_table)

        status_df, con = wwp.work_with_data(**{"type": "get", "con": con, "select": '*',
                                               "from": "last_download", "condition":
                                                   {"table_name": {sql_table: "="}}})
        if status_df.empty:
            cur = wwp.execute_many(cur, all_dt_dict.get(sql_table)[4], "last_download")
        else:
            cur = wwp.work_with_data(**{"type": "update", "cur": cur, "update": "last_download",
                                        "update_condition": {"last_update": {
                                            all_dt_dict.get(sql_table)[4].loc[0, 'last_update']: "="}},
                                        "condition": {"table_name": {sql_table: "="}}})
        cur.close()
        con.commit()
    con.close()


def create_table(dict_request: dict, dict_connect: dict):
    con = wwp.connect_postgre(dict_connect, 'main_base')
    # Цикл по всем запроссам
    for number_request in dict_request.keys():
        for sql_table in dict_request.get(number_request)['databases_tables'].split(', '):
            # Проверка наличия таблицы в БД
            con, found_table = wwp.get_table_name_from_postgre(con, sql_table)
            if found_table:
                # Если таблица есть, то проверим соответствие столбцов
                con = wwp.add_column_to_table(**{'con': con,
                                                 'sql_tab': sql_table,
                                                 'col_dict': dict_request.get(number_request).get('columns_info')})
            else:
                # Создадим таблицу
                con = wwp.add_table_to_bd(**{'con': con,
                                             'sql_tab': sql_table,
                                             'col_dict': dict_request.get(number_request).get('columns_info')})
    con.close()


def main(request):
    """
    Функция, в которой запускаются все "подпункции"
    :param request: Блок с типами данных и текстом запросса к 1С
    :return:
    """
    st = datetime.datetime.now()
    path = Path(os.path.realpath(__file__))
    data_con_file = gcf.get_conf_file(path)
    databases_tables = data_con_file.get('questions_file').get(request).get('databases_tables')
    lg_file.write_to_log(path, f"Старт загрузки {databases_tables}.")

    all_data_dict = dict()
    try:
        v83 = connect_1c(data_con_file)  # Подключимся к 1С
    except Exception as e:
        lg_file.write_to_log(path, f"Ошибка подключения к серверу 1С.\n{e}")
        return
    else:
        # Изменим текст запроса, получим дату последней загрузки
        request_to_1c, previous_down_date = req_definition(data_con_file.get('questions_file'),
                                                           data_con_file.get('data_connect'), request)
        # df начала загрузки данных из 1С для использования в "Power BI"
        today_df = pd.DataFrame(data={'table_name': [databases_tables],
                                      'last_update': [str(datetime.datetime.today())]})
        # Выполним запросы к серверу 1С
        time_df, v83 = query_to_1c(v83, request_to_1c, data_con_file.get('questions_file')[request]['columns_info'])

        # Сохраним полученые данные как pickle объект
        spd.save(**{"catalog": "way_to_pickle",
                    "path": path,
                    "file_name": databases_tables,
                    "to_pickle": time_df})

        # Изменяем тип данных
        time_df = change_data_type_after_1c(data_con_file.get('questions_file')[request].get('columns_info'), time_df)

        # Сохраним полученые данные как pickle объект
        spd.save(**{"catalog": "way_to_pickle_after_change",
                    "path": path,
                    "file_name": databases_tables,
                    "to_pickle": time_df})

        type_of_key_column = None  # Тип столбца для таблиц "directories"
        # У таблиц "documents" не может быть None
        if data_con_file['questions_file'][request]['tables_type'] == 'documents':
            type_of_key_column = data_con_file['questions_file'][request]['columns_info'][
                data_con_file['questions_file'][request]['field_to_delete']]

        # Заполнение all_data_dict
        all_data_dict[databases_tables] = [data_con_file['questions_file'][request]['tables_type'],
                                           data_con_file['questions_file'][request]['field_to_delete'],
                                           time_df,
                                           previous_down_date,
                                           today_df,
                                           type_of_key_column]
        # Запишем данные в базу данных
        work_with_postgre(all_data_dict, data_con_file['data_connect'])

        lg_file.write_to_log(path, f"Затратили Всего времени на запрос {databases_tables} -"
                                   f" {datetime.datetime.now() - st}.")


def start_process():
    """
    Функция разделяет программу на потоки (кол-во указанно в файле настроек).
    Каждый поток поднимает COM объект с подключением к серверу 1С и выполняет свой запрос.

    :return:
    """
    p_st = Path(os.path.realpath(__file__))
    lg_file.write_to_log(p_st, f"Start download")
    data_con_f = gcf.get_conf_file(p_st)
    create_table(data_con_f.get('start_work'), data_con_f.get('data_connect'))
    create_table(data_con_f.get('questions_file'), data_con_f.get('data_connect'))
    # Получим кол-во процессов
    concur_reg = data_con_f.get('data_connect').get('advanced_settings').get('processes')

    with Pool(concur_reg) as proc:
        proc.map(main, range(len(data_con_f.get('questions_file'))))
    """
    # Для отладки
    for number in range(len(data_con_f.get('questions_file'))):
        main(number)
    """
    lg_file.write_to_log(p_st, f"Finish download\n\n")


if __name__ == '__main__':
    p = Path(os.path.realpath(__file__))
    lg_file.write_to_log(p, f"Program started at.")
    # Вид запуска
    type_period = gcf.get_conf_file(p).get('data_connect').get('scheduler').get('period')
    # частота запуска (перезапуска)
    time_interval = gcf.get_conf_file(p).get('data_connect').get('scheduler').get('time')
    """
    # Для отладки
    start_process()
    scheduler = BackgroundScheduler()
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(start_process, type_period, seconds=time_interval)
    """
    # Для отладки
    scheduler.add_job(start_process, type_period, seconds=600)
    """
    scheduler.start()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('system exit')
    except Exception as e:
        print(e)
    finally:
        print('end program')
