import os
import glob

# Путь к директории с HTML-файлами. Замените на свой путь.
directory = r'Q:\Users\Andrew\Downloads\slivmilana-main\new'

# Старый домен и новый домен
old_domain = 'anonymedates.icu'
new_domain = 'test26.shop'

# Находим все .html файлы в директории
html_files = glob.glob(os.path.join(directory, '*.html'))

for file_path in html_files:
    try:
        # Читаем содержимое файла
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Заменяем старый домен на новый
        new_content = content.replace(old_domain, new_domain)
        
        # Если содержимое изменилось, перезаписываем файл
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Обновлен файл: {file_path}")
        else:
            print(f"Нет изменений в файле: {file_path}")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")