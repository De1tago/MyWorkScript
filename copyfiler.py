import os
import shutil

# Список файлов для копирования
files_to_copy = ['b2r.m', 'oomf2matlab.m', 'b_mag_simple.m']

# Диапазон номеров папок
start_folder = 5.51
end_folder = 5.90
step = 0.01

# Перебираем диапазон номеров папок с шагом 0.01
current_folder = start_folder
while current_folder <= end_folder:
    # Формируем имя папки
    folder_name = f'squre_oomsv_b_mag_f_{current_folder:.2f}'

    # Проверяем, существует ли папка
    if not os.path.exists(folder_name):
        # Создаем папку, если она не существует
        os.makedirs(folder_name)

    # Копируем каждый файл в папку
    for file_name in files_to_copy:
        # Формируем полный путь к файлу назначения
        destination_path = os.path.join(folder_name, file_name)
        # Копируем файл
        shutil.copy(file_name, destination_path)
        print(f'Файл {file_name} скопирован в {destination_path}')

    # Увеличиваем номер папки на шаг
    current_folder += step

print("Копирование завершено.")
