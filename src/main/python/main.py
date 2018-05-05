from data_collection.data_collector import DataCollector
from config import auth_keys

if __name__ == '__main__':
    search_params = {
        'words': ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#iot']
    }

    data_collector = DataCollector(search_params=search_params, auth_keys=auth_keys)
    data_collector.run_collection()
