import pytest
from checkout import checkout

from yaml_reader import data


class TestPositive:
    @staticmethod
    def check_7z_a(cmd_params, test_params):
        assert checkout(
            f"cd {data.get('folder_in')}; {cmd_params} {data.get('folder_out')}archive",
            'Everything is Ok'
        ), f'{test_params["name"]} fail'

    @staticmethod
    def check_7z_d(cmd_params, test_params):
        assert checkout(
            f"cd {data.get('folder_out')}; {cmd_params} ./archive.7z file1.txt",
            'Everything is Ok'
        ), f'{test_params["name"]} fail'

    @staticmethod
    def check_7z_l(cmd_params, test_params):
        assert checkout(
            f"cd {data.get('folder_out')}; {cmd_params} ./archive.7z",
            'Listing archive: ./archive.7z'
        ), f'{test_params["name"]} fail'

    def run_test(self, test_name):
        test_params = data['tests'][test_name]
        cmd = test_params['cmd']
        params = test_params['params']

        mapper = {
            'test_7z_a': self.check_7z_a,
            'test_7z_d': self.check_7z_d,
            'test_7z_l': self.check_7z_l
        }

        return mapper[test_name](cmd_params=cmd, test_params=params)

    def test_step1(self):
        assert checkout('cat /etc/os-release', 'jammy'), 'test1 fail'

    def test_step2(self):
        assert checkout('cat /etc/os-release', '22.04.1'), 'test2 fail'

    def test_step3(self):
        assert checkout('cat /etc/os-release', 'NAME'), 'test3 fail'

    def test_7z_a(self, make_folders, make_files):
        self.run_test('test_7z_a')

    def test_7z_d(self, make_folders, make_files):
        self.run_test('test_7z_d')

    def test_7z_l(self, make_folders, make_files):
        self.run_test('test_7z_l')


if __name__ == '__main__':
    pytest.main(['-vv'])