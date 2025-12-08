#!/usr/bin/env python3
"""
transliterate_links_and_rename.py

Как пользоваться (рекомендуемый порядок):
1) Создать ветку: git checkout -b transliteration
2) Установить зависимости: pip install unidecode
3) Запустить в режиме dry-run (не будет менять файлы, только покажет что бы сделал):
   python transliterate_links_and_rename.py --dry-run
4) Если всё ок — запустить без --dry-run:
   python transliterate_links_and_rename.py
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote, quote

try:
    from unidecode import unidecode
except Exception:
    print("Please install dependency: pip install Unidecode")
    sys.exit(1)

PAGES_DIR = Path("pages")  # папка с твоими страницами
EXT = ".html"

# slugify: transliterate (unidecode), lower, replace non-alnum with -, strip duplicates
def slugify(s: str) -> str:
    s = unidecode(s)  # кириллица -> латиница
    s = s.lower()
    # replace spaces and separators with hyphen
    s = re.sub(r"[^\w\s-]", "", s)               # remove punctuation except underscore
    s = re.sub(r"[\s_]+", "-", s)                # spaces/underscores -> hyphen
    s = re.sub(r"-{2,}", "-", s)                 # collapse multiple hyphens
    s = s.strip("-")
    if not s:
        s = "page"
    return s

# Получить базовое имя файла без extension, и вернуть декодированный и slugified варианты
def compute_new_name(file_path: Path) -> str:
    name = file_path.name
    if name.lower().endswith(EXT):
        name_base = name[:-len(EXT)]
    else:
        name_base = name
    # try decode percent-encoding
    decoded = unquote(name_base)
    # also try decoding twice (на случай двойной кодировки)
    decoded2 = unquote(decoded)
    source_text = decoded2 if decoded2 != decoded else decoded
    # strip leading slashes if present
    source_text = source_text.lstrip("/")
    # slugify
    slug = slugify(source_text)
    return slug + EXT

# find links to replace inside file content; return regex-safe patterns
def variants_for_old_path(old_rel_path: str):
    # old_rel_path может быть с кириллицей или закодированным
    # создаём варианты: raw, unquoted, quoted
    raw = old_rel_path
    unq = unquote(raw)
    q = quote(unq, safe="/:?#[]@!$&'()*+,;=%")  # стандартное quote; but keep slashes
    # also percent-encoded original (if input was decoded)
    q2 = quote(raw, safe="/:?#[]@!$&'()*+,;=%")
    variants = set([raw, unq, q, q2])
    # also add variants without leading slash
    v2 = set()
    for v in variants:
        if v.startswith("/"):
            v2.add(v[1:])
    variants = variants.union(v2)
    return sorted(list(variants), key=len, reverse=True)  # длинные сначала

def main(dry_run: bool, do_git_mv: bool, update_all_files: bool):
    if not PAGES_DIR.exists():
        print(f"ERROR: folder {PAGES_DIR} not found. Проверь путь.")
        sys.exit(1)

    # 1) Сканируем файлы в pages/
    page_files = sorted([p for p in PAGES_DIR.iterdir() if p.is_file() and p.suffix.lower() == EXT])
    if not page_files:
        print("No html files found in pages/. Проверь содержимое.")
        sys.exit(0)

    # 2) Собираем маппинг старое имя -> новое имя (без конфликтов)
    mapping = {}
    collisions = {}
    for p in page_files:
        new_name = compute_new_name(p)
        if new_name == p.name:
            continue
        dst = PAGES_DIR / new_name
        # если новый уже создан, добавить индекс
        if dst.exists() or new_name in mapping.values():
            # найдём свободный суфикс
            base = new_name[:-len(EXT)]
            i = 1
            while True:
                candidate = f"{base}-{i}{EXT}"
                if not (PAGES_DIR / candidate).exists() and candidate not in mapping.values():
                    new_name = candidate
                    break
                i += 1
        mapping[p.name] = new_name

    if not mapping:
        print("Нечего переименовывать — все имена уже в латинице/slug-подобные.")
    else:
        print(f"Found {len(mapping)} files to rename.")
        for k, v in mapping.items():
            print(f"  {k} -> {v}")

    # 3) Составляем список всех файлов, где нужно заменить ссылки
    # Если update_all_files==False — обновляем только файлы в /pages. Если True — весь репозиторий.
    if update_all_files:
        all_text_files = [p for p in Path(".").rglob("*") if p.is_file() and p.suffix.lower() in {".html", ".htm", ".md", ".txt"}]
    else:
        all_text_files = [p for p in PAGES_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".html", ".htm", ".md", ".txt"}]

    # 4) Готовим замены: для каждый старый файл - генерируем варианты старого пути и новый путь
    replacements = []  # tuples (file_pattern_variants_list, new_rel_path)
    for old_name, new_name in mapping.items():
        # old relative path used in links: maybe "/pages/old.html" or "/old.html" or just "old.html"
        # здесь предполагаем, что ссылки у тебя выглядят как https://www.slivmilana.ru/<path>
        # но для универсальности подготовим варианты:
        old_rel = f"/pages/{old_name}"
        old_rel_root = f"/{old_name}"
        old_rel_no_slash = old_name
        new_rel_root = f"/pages/{new_name}"
        new_rel_root2 = f"/{new_name}"  # если проект отдаёт из корня
        # get variants for each old path
        vars1 = variants_for_old_path(old_rel)
        vars2 = variants_for_old_path(old_rel_root)
        vars3 = variants_for_old_path(old_rel_no_slash)
        vars_all = sorted(set(vars1 + vars2 + vars3), key=len, reverse=True)
        # new target: decide what to insert in links — используем new_rel_root (pages/)
        # but многие сайты используют site-root '/<slug>.html' — оставлю оба возможными replacements
        replacements.append((vars_all, new_rel_root))  # primary
        replacements.append((vars_all, new_rel_root2))  # alternative

    # 5) Dry-run: показать, где и какие замены будут сделаны
    if dry_run:
        print("\n--- DRY RUN: показать потенциальные изменения (не меняем файлы) ---\n")
    changes_to_apply = {}

    for f in all_text_files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            # skip binary or unreadable
            continue
        original = text
        changed = text
        for variants_list, new_target in replacements:
            for old_variant in variants_list:
                # заменим все вхождения старой ссылки на новую (сохраняя возможный префикс сайта)
                # 1) https://www.slivmilana.ru/OLD -> https://www.slivmilana.ru/NEW
                changed = re.sub(re.escape(f"https://www.slivmilana.ru{old_variant}"), f"https://www.slivmilana.ru{new_target}", changed)
                # 2) /OLD -> /NEW
                changed = re.sub(re.escape(old_variant), new_target, changed)
        if changed != original:
            changes_to_apply[f] = (original, changed)
            print(f"[WILL CHANGE] {f} - {sum(1 for _ in re.finditer('.', '') )}")  # dummy to show line
    if dry_run:
        print("\nDry-run finished. Files that will be modified listed above.")
        if not changes_to_apply and not mapping:
            print("Ничего не обнаружено для замены.")
        else:
            print("Если всё ок — запустите скрипт без --dry-run чтобы изменить файлы и выполнить git mv/commit.")
        return

    # 6) Применяем изменения: редактируем файлы
    for f, (orig, newtxt) in changes_to_apply.items():
        print(f"Updating {f}")
        f.write_text(newtxt, encoding="utf-8")

    # 7) Переименовываем файлы (git mv если возможно)
    for old, new in mapping.items():
        oldp = PAGES_DIR / old
        newp = PAGES_DIR / new
        if not oldp.exists():
            print(f"Warning: {oldp} not found during rename step.")
            continue
        if newp.exists():
            print(f"Warning: target {newp} already exists, skipping rename.")
            continue
        if do_git_mv:
            # try git mv
            rc = os.system(f'git mv "{oldp}" "{newp}"')
            if rc != 0:
                print(f"git mv failed for {old} -> {new}, doing os.rename")
                shutil.move(str(oldp), str(newp))
        else:
            shutil.move(str(oldp), str(newp))
        print(f"Renamed {old} -> {new}")

    # 8) git add/commit
    print("Staging and committing changes...")
    os.system('git add -A')
    commit_msg = f"Transliterate filenames and update links: {len(mapping)} files"
    rc = os.system(f'git commit -m "{commit_msg}" || true')
    if rc == 0:
        print("Committed changes.")
    else:
        print("No commit created (maybe nothing to commit).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Don't modify files, just show what would change")
    parser.add_argument("--no-git-mv", action="store_true", help="Don't use git mv (use plain file moves)")
    parser.add_argument("--all", action="store_true", help="Update links across the whole repo, not only /pages")
    args = parser.parse_args()
    main(dry_run=args.dry_run, do_git_mv=not args.no_git_mv, update_all_files=args.all)
