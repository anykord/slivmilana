import os
from datetime import datetime

# === НАСТРОЙКИ ===
BASE_URL = "https://www.slivmilana.ru"
PAGES_DIR = "pages"                    # папка с html-файлами
OUTPUT_FILE = "sitemap.xml"            # куда сохраняем
MAX_URLS_PER_SITEMAP = 45000           # лимит (у тебя 2400 — ок)
TODAY = datetime.now().strftime("%Y-%m-%d")

# === ГЕНЕРАЦИЯ ===
def generate_sitemap():
    if not os.path.isdir(PAGES_DIR):
        print(f"Ошибка: папка {PAGES_DIR} не найдена!")
        return

    files = [f for f in os.listdir(PAGES_DIR) if f.lower().endswith('.html')]
    print(f"Найдено файлов: {len(files)}")

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # главная страница
    sitemap_content += f"""  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>\n"""

    # все страницы из /pages/
    for filename in sorted(files):
        page_url = f"{BASE_URL}/pages/{filename.replace('.html', '')}"  # cleanUrls убирает .html
        sitemap_content += f"""  <url>
    <loc>{page_url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

    sitemap_content += '</urlset>'

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print(f"ГОТОВО! sitemap.xml создан → {len(files) + 1} URL")
    print(f"   → {BASE_URL}/sitemap.xml")
    print("\nТеперь залей:")
    print("   git add sitemap.xml")
    print("   git commit -m \"Update sitemap.xml for latin URLs\"")
    print("   git push origin main")

if __name__ == "__main__":
    generate_sitemap()
