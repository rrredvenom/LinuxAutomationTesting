"""
Задание 1.

Условие:
Написать функцию на Python, которой передаются в качестве параметров команда и текст.
Функция должна возвращать True,
если команда успешно выполнена и текст найден в её выводе и False в противном случае.
Передаваться должна только одна строка, разбиение вывода использовать не нужно.

Задание 2. (повышенной сложности)

Доработать функцию из предыдущего задания таким образом,
чтобы у неё появился дополнительный режим работы,
в котором вывод разбивается на слова с удалением всех знаков пунктуации
(их можно взять из списка string.punctuation модуля string).
В этом режиме должно проверяться наличие слова в выводе.
"""
import subprocess
import string


def is_word_in_command_output(command: str, word: str, split_mode=False) -> str | bool:
    """ Check if word is in command output.

    :param command: command to execute.
    :param word: word to check in output.
    :param split_mode: mode to clear punctuation for check.
    :return: word if found, else False.
    """
    try:
        completed_process = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            text=True
        )

        if not completed_process.returncode:
            output = completed_process.stdout

            if split_mode:
                output = ''.join(char if char not in string.punctuation else ' ' for char in output)
                words = output.split()
                return word in words
            else:
                return word in output

        else:
            return False

    except Exception as e:
        print(f'Error: {str(e)}')
        return False


command_to_run = 'cat /etc/os-release'
word_to_check = 'Ubuntu'
split_mode_enabled = True

result = is_word_in_command_output(command=command_to_run, word=word_to_check, split_mode=split_mode_enabled)
print(f"Word '{word_to_check}' found in command output: {result}")