#создать файл my_function.py с функциями greet & change_name
#принимает строку а возрващает изменённое имя где каждая вторая буква большая
#принимает строку ничего не возвращает а просто принтит Hello имя  Через Rich

from rich import print as rprint

def greet(value: str):
    rprint(f'[bold purple]Дарова, {value}!')

def change_name(value: str) -> str:
    chars = list(value)
    for i in range(len(chars)):
        if i % 2 == 0:
            chars[i] = chars[i].upper()
    value = ''.join(chars)
    return value