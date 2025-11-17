import os
from datetime import datetime

# === НАСТРОЙКИ ===
DOMAIN = "https://www.slivmilana.ru"
OUTPUT_DIR = "."  # Папка с index.html и pages/
SITEMAP_PATH = os.path.join(OUTPUT_DIR, "sitemap.xml")

# === СОБИРАЕМ ВСЕ URL ===
urls = []

# 1. Главная
urls.append(DOMAIN + "/")

# 2. Все HTML-файлы в корне (кроме sitemap, robots)
for file in os.listdir(OUTPUT_DIR):
    if file.endswith(".html") and file not in ["sitemap.xml", "robots.txt"]:
        urls.append(f"{DOMAIN}/{file}")

# 3. Все страницы в /pages/
pages_dir = os.path.join(OUTPUT_DIR, "pages")
if os.path.exists(pages_dir):
    for file in os.listdir(pages_dir):
        if file.endswith(".html"):
            urls.append(f"{DOMAIN}/pages/{file}")

# 4. robots.txt (опционально)
urls.append(f"{DOMAIN}/robots.txt")

# === ГЕНЕРИРУЕМ SITEMAP.XML ===
today = datetime.now().strftime("%Y-%m-%d")

with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    
    # Главная — приоритет 1.0
    f.write(f'  <url>\n    <loc>{DOMAIN}/</loc>\n    <lastmod>{today}</lastmod>\n    <priority>1.0</priority>\n  </url>\n')
    
    # Остальные страницы — приоритет 0.8
    for url in urls[1:]:  # пропускаем главную (уже добавлена)
        if url.endswith("robots.txt"):
            priority = "0.5"
        else:
            priority = "0.8"
        f.write(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{priority}</priority>\n  </url>\n')
    
    f.write('</urlset>')

print(f"ГОТОВО! Sitemap перегенерирован: {SITEMAP_PATH}")
print(f"URL в sitemap: {len(urls)}")