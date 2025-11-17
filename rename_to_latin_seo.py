import os
import re
from urllib.parse import quote

# === НАСТРОЙКИ ===
PAGES_DIR = "pages"  # Папка с твоими HTML-файлами
BACKUP = True        # Создать бэкап старых имён (рекомендую)

# Словарь транслита (SEO-дружелюбный: коротко, читаемо)
TRANSLIT_DICT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    ' ': '-', '—': '-', '_': '-', '+': '-', '?': '', '!': '', '.': ''
}

# === ФУНКЦИЯ ТРАНСЛИТА ===
def translit_seo(filename):
    name, ext = os.path.splitext(filename)
    name = name.lower()
    
    # Транслит
    new_name = ''
    for char in name:
        new_name += TRANSLIT_DICT.get(char, char)
    
    # SEO: убираем лишнее, оставляем дефисы
    new_name = re.sub(r'[^a-z0-9-]', '', new_name)
    new_name = re.sub(r'-+', '-', new_name)  # множественные дефисы → один
    new_name = new_name.strip('-')
    
    # Максимум 100 символов (Vercel лимит)
    if len(new_name) > 90:
        new_name = new_name[:90]
    
    return new_name + ext

# === ОСНОВНОЙ КОД ===
if not os.path.exists(PAGES_DIR):
    print(f"Папка {PAGES_DIR} не найдена!")
    exit()

files = [f for f in os.listdir(PAGES_DIR) if f.endswith('.html')]
print(f"Найдено файлов: {len(files)}")

renamed = 0
backup_map = {}

for old_name in files:
    new_name = translit_seo(old_name)
    
    if new_name == old_name:
        continue  # уже на латинице
    
    old_path = os.path.join(PAGES_DIR, old_name)
    new_path = os.path.join(PAGES_DIR, new_name)
    
    # Избегаем коллизий
    counter = 1
    base, ext = os.path.splitext(new_name)
    while os.path.exists(new_path):
        new_name = f"{base}-{counter}{ext}"
        new_path = os.path.join(PAGES_DIR, new_name)
        counter += 1
    
    os.rename(old_path, new_path)
    backup_map[old_name] = new_name
    renamed += 1
    print(f"✓ {old_name} → {new_name}")

# === БЭКАП (опционально) ===
if BACKUP and renamed > 0:
    with open("rename_backup.txt", "w", encoding="utf-8") as f:
        for old, new in backup_map.items():
            f.write(f"{old} → {new}\n")
    print(f"\nБэкап сохранён в rename_backup.txt ({renamed} файлов)")

print(f"\nГОТОВО! Переименовано: {renamed} файлов")
print("Залей на GitHub → Vercel обновит → 404 исчезнут!")