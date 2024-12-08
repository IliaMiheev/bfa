import py7zr
import pyzipper
import os

def open_arch(zip_path, password=None):
    """
    Открывает архив (ZIP или 7z) и извлекает его содержимое.

    :param zip_path: Путь к архиву (ZIP или 7z)
    :param password: Пароль для извлечения файлов из архива (по умолчанию None)
    """
    password = str(password)
    # Проверяем расширение архива
    if zip_path.endswith('.zip'):
        # Обработка ZIP архива
        try:
            with pyzipper.AESZipFile(zip_path, 'r') as zip_ref:
                if password:
                    zip_ref.setpassword(password.encode('utf-8'))
                zip_ref.extractall()
                return 1
        except Exception as e:
            pass

    elif zip_path.endswith('.7z'):
        # Обработка 7z архива
        try:
            with py7zr.SevenZipFile(zip_path, mode='r', password=password) as seven_zip_ref:
                seven_zip_ref.extractall()
                return 1
        except Exception as e:
            pass
    
    else:
        print("\033[91mПоддерживаются только ZIP и 7z архивы\033[0m")
    return 0

# Определяем архив в текущей директории
def get_archive_name():
    current_directory = os.path.dirname(os.path.abspath(
        __file__))  # Получаем путь к текущей директории
    zip_archives = []  # Создаем пустой список для хранения имен ZIP-архивов

    for file in os.listdir(current_directory):
        # Проходим по всем файлам в текущей директории
        if file.endswith('.zip') or file.endswith('.7z'):
            # Если файл имеет расширение .zip, добавляем его в список
            zip_archives.append(file)

    if len(zip_archives) == 0:
        print('\033[91mВ папке нет архивов. Распаковывать нечего')
        return 0  # Если ZIP-архивов не найдено
    elif len(zip_archives) == 1:
        # Если найден один ZIP-архив, возвращаем его имя
        return zip_archives[0]

    print('Введи q если хочешь отменить выполнение кода')
    print("Найдены следующие архивы:\n")
    for i, archive in enumerate(zip_archives):
        # Выводим список найденных ZIP-архивов с нумерацией
        print(f"{i+1}. {archive}")

    while True:
        choice = input("\nВыберите номер архива: ")
        if not choice.isdigit():
            if choice.lower() == 'q':
                print('\n\033[91mВыполнение кода приостановлено пользователем')
                return 0
            else:
                print("\033[91mНадо было ввести число, а не строку. Введи номер архива снова\033[0m")
        elif choice.isdigit():
            if 0 < int(choice) <= len(zip_archives):
                # Если введен корректный номер архива, возвращаем его имя
                return zip_archives[int(choice)-1]
            else:
                # Если введен некорректный номер, просим ввести снова
                print("\033[91mНет такого номера архива. Введи номер архива снова\033[0m")



def main():
    zip_path = get_archive_name()
    if zip_path == 0:
        exit()

    n = int(input('\nВведи число до которого будет осуществляться перебор: '))

    for num in range(n):
        print(num)
        if open_arch(zip_path=zip_path, password=num):
            print(f'\n\033[92mПароль от архива:', num)
            break
    else:
        print('\033[91mПароль не найден')

if __name__ == '__main__':
    main()
