from pathlib import Path

def base_path():
    return str(Path(__file__).parent.absolute())

def app_path(relative_path):
    return base_path() + '/' + relative_path

def data_path(relative_path, test_data=False):
    if test_data:
        relative_path = '/test_data/' + relative_path
    return base_path() + '/../data/' + relative_path

def conf_path(relative_path):
    return base_path() + '/../conf/' + relative_path

def models_path(relative_path):
    return data_path('/models/' + relative_path)

def signatures_path(relative_path):
    return data_path('/signatures/' + relative_path)
