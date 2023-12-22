import os

import pytest

from sshcheckers import *
from yaml_reader import data

#test
class TestDeploy:
    def test_deploy(self):
        res = []
        upload_files(
            data['host'],
            data['username'],
            data['password'],
            data['file_directory_path'],
            data['target_directory']
        )

        res.append(
            ssh_checkout(
                data['host'],
                data['username'],
                data['password'],
                "echo 'zf59am41' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                "Настраивается пакет"
            )
        )

        res.append(
            ssh_checkout(
                data['host'],
                data['username'],
                data['password'],
                "echo 'zf59am41' | sudo -S dpkg -s p7zip-full",
                "Status: install ok installed"
            )
        )
        assert all(res), "Ошибка деплоя"

    @pytest.mark.parametrize('host, user, password, port', [(data['host'], data['username'], data['password'], 22)])
    def test_ssh_checkout_positive(self, host, user, password, port):
        cmd = "echo 'Hello, world!'"
        text = "Hello, world!"
        assert ssh_checkout(host, user, password, cmd, text, port), "ssh_checkout_positive failed"

    @pytest.mark.parametrize('host, user, password, port', [(data['host'], data['username'], data['password'], 22)])
    def test_ssh_getout(self, host, user, password, port):
        cmd = "echo 'This is the output'"
        expected_output = "This is the output"
        assert ssh_getout(host, user, password, cmd, port).strip() == expected_output, "ssh_getout failed"

    @pytest.mark.parametrize('host, user, password, port', [(data['host'], data['username'], data['password'], 22)])
    def test_ssh_checkout_negative(self, host, user, password, port):
        cmd = "ls non_existent_directory"
        error_text = "No such file or directory"
        assert not ssh_checkout_negative(host, user, password, cmd, error_text, port), 'ssh_checkout_negative failed'

    @pytest.mark.parametrize(
        'host, user, password, local_path, remote_path, port',
        [
            (
                    data['host'],
                    data['username'],
                    data['password'],
                    data['file_directory_path'],
                    data['target_directory'],
                    22
            )
        ]
    )
    def test_upload_files(self, host, user, password, local_path, remote_path, port):
        upload_files(host, user, password, local_path, remote_path, port)
        cmd = "ls /home/user2/"
        text = "p7zip-full.deb"

        assert text in ssh_getout(host, user, password, cmd, port).strip(), 'upload_files failed'

    @pytest.mark.parametrize(
        'host, user, password, remote_path, local_path, port',
        [
            (
                    data['host'],
                    data['username'],
                    data['password'],
                    data['target_directory'],
                    data['file_directory_path_test'],
                    22
            )
        ]
    )
    def test_download_files(self, host, user, password, remote_path, local_path, port):
        download_files(host, user, password, remote_path, local_path, port)
        this_dir = os.getcwd()
        text = "p7zip-full.deb"

        assert text in os.listdir(f"{this_dir}/tests1/"), 'download_files failed'


if __name__ == '__main__':
    pytest.main(['-vv'])
