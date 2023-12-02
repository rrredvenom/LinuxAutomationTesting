"""
Доработать проект, добавив тест команды расчёта хеша (h).
Проверить, что хеш совпадает с рассчитанным командой crc32.
"""
from pathlib import Path
from typing import Annotated

import pytest
import subprocess
import tempfile


@pytest.fixture
def test_file():
    """
    Create a temporary directory for the test.
    :return: test file path.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        test_file_path = temp_dir_path / 'test_file.txt'
        with open(test_file_path, 'w', encoding='utf-8') as file:
            file.write('This is a test file content.')

        yield test_file_path

        test_file_path.unlink()


def test_hash_calculation(test_file: Annotated[str, pytest.fixture]):
    """
    Test: calculate the hash using the 'h' command and compare with crc32.
    :param test_file: fixture for file creation.
    """
    hash_command = f'7z h {test_file}'
    hash_output = subprocess.run(hash_command, shell=True, capture_output=True, text=True, encoding='utf-8')
    hash_result = hash_output.stdout

    crc32_match = hash_result[hash_result.find('data:'):].split()[1]

    crc32_command = f'crc32 {test_file}'
    crc32_output = subprocess.run(crc32_command, shell=True, capture_output=True, text=True, encoding='utf-8')
    crc32_result = crc32_output.stdout.strip().upper()

    assert crc32_match == crc32_result