import pickle
import get_catalogs_ways as gt
import gzip


def save(protocol=-1, **kwargs):
    path = kwargs.get('path')
    file_name = kwargs.get('file_name')
    catalog = kwargs.get('catalog')
    data = kwargs.get("to_pickle")
    way = gt.get_catalogs_way(path).get(catalog)

    with gzip.GzipFile(f'{way}\\{file_name}', 'wb') as file:
        pickle.dump(data, file, protocol)


def load(**kwargs) -> object:
    file_name = kwargs.get('file_name')
    catalog = kwargs.get('catalog')
    path = kwargs.get('path')
    way = gt.get_catalogs_way(path).get(catalog)

    with gzip.GzipFile(f'{way}\\{file_name}', 'rb') as file:
        load_data = pickle.load(file)

    return load_data
