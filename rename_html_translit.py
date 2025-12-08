import os
import re

# Транслит строго по вашему принципу
translit = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
    'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
    'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
    'ю': 'yu', 'я': 'ya'
}

def to_translit(text):
    result = ""
    for ch in text.lower():
        result += translit.get(ch, ch)  # оставляем символ, если не кириллица
    return result

# Используем текущую директорию
directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.lower().endswith('.html'):
        name, ext = os.path.splitext(filename)
        new_name = to_translit(name)

        # заменяем всё лишнее на дефис, убираем дубли и хвосты
        new_name = re.sub(r'[^a-z0-9]+', '-', new_name)  # не латиница/цифра → "-"
        new_name = re.sub(r'-+', '-', new_name)          # сжать "--" → "-"
        new_name = new_name.strip('-')                   # убрать "-" по краям

        new_filename = new_name + ext

        if filename != new_filename:
            print(f"{filename} → {new_filename}")
            os.rename(os.path.join(directory, filename),
                      os.path.join(directory, new_filename))

print("Готово! 🚀")
