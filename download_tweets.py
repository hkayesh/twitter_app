from data_collection.data_collector import DataCollector
from settings import AUTH_SETTINGS as auth_keys

if __name__ == '__main__':
    search_params = {
        'words': ['#cop25', '#cop25chile', '#cop25madrid', '#climateadaptation', '#climatechangeadaptation',
                  '#adaptation', '#climatechange']
    }

    data_collector = DataCollector(search_params=search_params, auth_keys=auth_keys)
    data_collector.run_collection()
