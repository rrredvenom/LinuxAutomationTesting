import time

from pytest import fixture

from yaml_reader import data
from checkout import checkout


@fixture(scope='module')
def make_folders():
    yield checkout(f'mkdir -p {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")}', '')
    checkout(f'rm -rf {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")}', '')


@fixture
def make_files():
    files_to_create = data.get('files', [])
    file_creation_command = ' '.join([f'touch {file}' for file in files_to_create])
    return checkout(f'cd {data.get("folder_in")}; {file_creation_command}', '')


@fixture(autouse=True)
def write_test_statistics():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    num_files = len(data.get('files', []))
    file_size = data.get('file_size', 0)

    with open('/proc/loadavg', 'r') as loadavg_file:
        processor_load = loadavg_file.read()

    statistics_line = (
        f'Timestamp: {timestamp}\n'
        f'Number of Files: {num_files}\n'
        f'File Size: {file_size} bytes\n'
        f'Processor Load Statistics:\n{processor_load}'
    )

    # Append the line to the stat.txt file
    with open(data.get('stat_file'), 'a') as stat_file:
        stat_file.write(statistics_line + '\n')

    yield