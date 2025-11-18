// clean-title.js — убирает запятые, точки, тире в конце title и h1
document.addEventListener("DOMContentLoaded", () => {
    // Чиним <title>
    document.title = document.title
        .replace(/[,.\s—\-_]+/g, ' ')   // все лишние знаки → один пробел
        .replace(/\s+/g, ' ')          // множественные пробелы → один
        .replace(/^\s+|\s+$/g, '')     // обрезаем пробелы по краям
        .trim();

    // Если в конце остался мусор — обрезаем до последнего нормального слова
    document.title = document.title.replace(/[^а-яА-Яa-zA-Z0-9]\s*$/, '').trim();

    // Добавляем красивый постфикс (можно убрать, если не нужен)
    if (!document.title.includes("Telegram")) {
        document.title += " — эксклюзив в Telegram";
    }

    // Чиним <h1>
    const h1 = document.querySelector('h1');
    if (h1) {
        h1.textContent = h1.textContent
            .replace(/[,.\s—\-_]+/g, ' ')
            .replace(/\s+/g, ' ')
            .replace(/^\s+|\s+$/g, '')
            .trim();
    }

    // Чиним все ссылки в блоке "Похожие запросы" (убираем ,,, в конце)
    document.querySelectorAll('a').forEach(link => {
        if (link.textContent.includes(',,')) {
            link.textContent = link.textContent
                .replace(/[,.\s—\-_]+/g, ' ')
                .replace(/\s+/g, ' ')
                .trim();
        }
    });
});
