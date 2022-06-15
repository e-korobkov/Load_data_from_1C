import psycopg2
import pandas as pd


def connect_postgre(dict_connect: dict, base_name: str) -> psycopg2.connect:
    """
    Функция устанавливающая подключение с базой данных.

    :param dict_connect: Данные для подключения.
    :param base_name: Имя базы данных
    :return: Объект подключения
    """
    con = psycopg2.connect(
        database=dict_connect.get(base_name).get("database"),
        user=dict_connect.get(base_name).get("user"),
        password=dict_connect.get(base_name).get("password"),
        host=dict_connect.get(base_name).get("host"),
        port=dict_connect.get(base_name).get("port")
    )
    return con


def get_table_name_from_postgre(con: psycopg2.connect, table_name) -> (psycopg2.connect, bool):
    """ 
    Проверим наличие таблицы в БД.
    Если таблица Присутствует в БД, то вернем True
    если таблицы нет, то вернет False 
    """
    cur = con.cursor()
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    cur.execute(sql)
    tables = cur.fetchall()

    for elem in tables:
        if table_name in elem:
            cur.close()
            return con, True
    cur.close()
    return con, False


def add_table_to_bd(**data):
    """
    Функция создает таблицы в базе данных
    """
    con = data.get('con')
    cur = con.cursor()
    sql_tab = data.get('sql_tab')
    time_list = list()

    # Проверка на тип входящих данных
    if isinstance(data.get('col_dict'), dict):
        col_dict = data.get('col_dict')
        for column in col_dict.keys():
            text = f'"{column.lower()}" {col_dict.get(column)}'
            time_list.append(text)
    elif isinstance(data.get('data_df'), pd.DataFrame):
        df = data.get('data_df')
        for col_num in range(len(df.columns)):
            column = df.columns[col_num]
            text = f'"{column.lower()}" text'
            time_list.append(text)
    text = ', '.join(time_list)

    cur.execute(f'CREATE TABLE public."{sql_tab}" ({text})')
    cur.close()
    con.commit()
    return con


def add_column_to_table(**data) -> psycopg2.connect:
    """
    Функция добавляет столбцы в таблицу
    """
    c = data.get('con')
    sql_tab = data.get('sql_tab')
    cr = c.cursor()
    # Получим перечень столбцов из БД
    q = f"SELECT column_name FROM information_schema.columns WHERE table_schema='public' and table_name='{sql_tab}'"
    cr.execute(q)
    time_data = cr.fetchall()
    cr.close()
    time_data2 = list()
    for num in time_data:
        time_data2.append(num[0])

    # Ветвление в зависимости от переданных в функцию данных
    # Получим перечень столбцов из dict
    if isinstance(data.get('col_dict'), dict):
        col_dict = data.get('col_dict')
        time_list = list(col_dict.keys())
        time_list_type = list(col_dict.values())
    # Получим перечень столбцов из DataFrame
    elif isinstance(data.get('data_df'), pd.DataFrame):
        df = data.get('data_df')
        time_list = list(df.columns)
        time_list_type = ['text'] * len(df)

    for num in range(len(time_list)):
        if time_list[num].lower() not in time_data2:
            col_name = time_list[num].lower()
            col_type = time_list_type[num].lower()
            q = f'ALTER TABLE "{sql_tab}" ADD COLUMN "{col_name}" {col_type};'
            cr = c.cursor()
            cr.execute(q)
            cr.close()
            c.commit()
    return c


# Проверить изспользование, если не используется то удалить
def drop_from_postgre(**data) -> psycopg2.connect:
    cur = data.get('cur')
    sql_table = '"' + data.get('sql_tab') + '"'
    data_list = data.get('data_list')

    if data_list[0] == 'documents':
        data_list[2] = '"' + data_list[2] + '"'
        sql_query = f"DELETE FROM {sql_table} WHERE {data_list[2]} = '{data_list[1]}';"
    elif data_list[0] == 'directories':
        sql_query = f"DELETE FROM {sql_table};"

    if sql_query:
        cur.execute(sql_query)
    return cur


def execute_many(cr: object, df: object, table_name: str) -> psycopg2.connect:
    table_name = '"' + table_name + '"'

    # Если нужна автонумерация bigserial
    if 'row_index' in df.columns:
        df = df.drop(columns=['row_index'])

    tuples = [tuple(x) for x in df.to_numpy()]

    cols = '","'.join(list(df.columns))
    cols = '"' + cols + '"'
    cols = cols.lower()
    query = f'INSERT INTO public.{table_name}({cols}) VALUES({"%s," * (df.values.shape[1] - 1)}{"%s" * 1})'
    cr.executemany(query, tuples)
    return cr


def make_request_string(data):
    """
    Функция строит сложные по структуре запросы
    """
    if isinstance(data.get('select'), str):
        q = 'select'
        # Дополнительное условие для select
        if data.get('add_cond'):
            q = f"{q} {data.get('add_cond')} {data.get('select')} from {data.get('from')}"
        else:
            q = f"{q} {data.get('select')} from {data.get('from')}"
    elif isinstance(data.get('delete'), str):
        q = f"delete from {data.get('delete')}"
    elif isinstance(data.get('update'), str):
        q = f"update {data.get('update')}"
        find_key = {'update_condition': "set"}

    def m_req(q_string, d, f_key):
        t_key = list(f_key.keys())[0]
        time_list = list()
        for key in d.get(t_key).keys():
            if isinstance(d.get(t_key).get(key), dict):
                t_key2 = list(d.get(t_key).get(key).keys())[0]
                time_str = f"{key} {d.get(t_key).get(key).get(t_key2)} '{t_key2}'"
                time_list.append(time_str)
        else:
            time_str_2 = f" {d.get(t_key).get('relationship')} ".join(time_list)
            q_string = f"{q_string} {f_key.get(t_key)} {time_str_2}"

        return q_string

    if isinstance(data.get('update_condition'), dict):
        q = m_req(q, data, find_key)
    if isinstance(data.get('condition'), dict):
        find_key = {'condition': "where"}
        q = m_req(q, data, find_key)
    return q


def work_with_data(**data):
    q = make_request_string(data)
    if data.get('type') == 'get':
        con = data.get('con')
        orders = pd.read_sql(q, con)
        return orders, con
    else:
        cur = data.get('cur')
        cur.execute(q)
        return cur
