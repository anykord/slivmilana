import os
from datetime import datetime

# Настройки
PAGES_DIR = "pages"
IMAGE_URL = "/loading-forever.jpg"        # путь от корня сайта
TG_LINK = "https://t.me/+6FpSw688td1hODQy"   # твой канал

# HTML-блок, который будем вставлять перед </body>
INSERT_BLOCK = f'''
<div style="max-width:640px;margin:30px auto;text-align:center;">
  <div style="position:relative;display:inline-block;">
    <img src="{IMAGE_URL}" style="width:100%;max-width:600px;border-radius:16px;filter:blur(25px);">
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.85);color:white;padding:20px 30px;border-radius:16px;font-size:18px;line-height:1.5;">
      Загрузка эксклюзивного фото...<br>
      <div style="font-size:28px;font-weight:bold;color:#ff6b6b;margin:10px 0;" id="timer">30</div>
      <b>Если фото не загрузилось — переходи в приватный канал ↓</b>
    </div>
  </div>
  <div style="margin-top:30px;">
    <a href="{TG_LINK}" target="_blank" style="display:inline-block;padding:16px 40px;background:#0088cc;color:white;font-size:20px;border-radius:12px;text-decoration:none;">
      Перейти в канал (бесплатно, 18+)
    </a>
  </div>
</div>

<script>
let sec = 30;
const t = document.getElementById('timer');
const int = setInterval(() => {
  sec--;
  t.textContent = sec;
  if (sec <= 0) clearInterval(int);
}, 1000);
</script>
'''

# Обходим все .html в pages/
count = 0
for filename in os.listdir(PAGES_DIR):
    if filename.lower().endswith('.html'):
        filepath = os.path.join(PAGES_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Если уже есть наш блок — пропускаем
        if "loading-forever" in content or "id=\"timer\"" in content:
            continue
            
        # Вставляем прямо перед </body>
        if '</body>' in content:
            content = content.replace('</body>', INSERT_BLOCK + '\n</body>')
        else:
            content += INSERT_BLOCK
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"ГОТОВО! Добавлено в {count} страниц из {len([f for f in os.listdir(PAGES_DIR) if f.endswith('.html')])}")
