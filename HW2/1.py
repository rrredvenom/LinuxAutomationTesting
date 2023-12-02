"""
Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).
"""
import os
import subprocess
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
TEST_DIR = os.path.join(DATA_DIR, 'test_dir')
ARCHIVE_FILE = os.path.join(DATA_DIR, 'test_archive.7z')


def create_test_archive() -> None:
    """
    Create some sample files in the TEST_DIR.
    """
    os.makedirs(TEST_DIR, exist_ok=True)
    with open(os.path.join(TEST_DIR, 'file1.txt'), 'w', encoding='utf-8') as file1:
        file1.write('This is file1 content.')
    with open(os.path.join(TEST_DIR, 'file2.txt'), 'w', encoding='utf-8') as file2:
        file2.write('This is file2 content.')
    os.makedirs(os.path.join(TEST_DIR, 'sub_dir'), exist_ok=True)
    with open(os.path.join(TEST_DIR, 'sub_dir/file3.txt'), 'w', encoding='utf-8') as file3:
        file3.write('This is file3 content.')

    try:
        subprocess.run(f'7z a {ARCHIVE_FILE} {TEST_DIR}', shell=True, check=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        print(f'Error creating the test archive: {e}')
        raise


@pytest.fixture(scope='module', autouse=True)
def setup_teardown():
    create_test_archive()
    yield
    os.remove(ARCHIVE_FILE)


def test_list_files_in_archive():
    """ Test: List files in the test archive. """
    result = subprocess.run(
        f'7z l {ARCHIVE_FILE}',
        shell=True,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
        encoding='utf-8'
    )
    assert 'file1.txt' in result.stdout
    assert 'file2.txt' in result.stdout
    assert 'sub_dir/file3.txt' in result.stdout


def test_extract_files_from_archive():
    """ Test: Extract files from the test archive to a temporary directory. """
    temp_dir = os.path.join(DATA_DIR, 'temp_dir')
    os.makedirs(temp_dir, exist_ok=True)
    subprocess.run(f'7z x -y {ARCHIVE_FILE} -o{temp_dir}', shell=True, check=True, encoding='utf-8')

    assert os.path.exists(os.path.join(temp_dir, 'test_dir'))

    extracted_files = os.listdir(os.path.join(temp_dir, 'test_dir'))
    print(f'Extracted files in {os.path.join(temp_dir, "test_dir")}: {extracted_files}')

    assert 'file1.txt' in extracted_files
    assert 'file2.txt' in extracted_files
    assert 'sub_dir' in extracted_files
    assert os.path.exists(os.path.join(temp_dir, 'test_dir/sub_dir/file3.txt'))