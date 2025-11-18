document.addEventListener("DOMContentLoaded", () => {
    document.title = document.title
        .replace(/[,.\s—\-_]+/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    if (!document.title.includes("Telegram")) {
        document.title += " — эксклюзив в Telegram";
    }
    const h1 = document.querySelector('h1');
    if (h1) {
        h1.textContent = h1.textContent
            .replace(/[,.\s—\-_]+/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }
    document.querySelectorAll('a').forEach(a => {
        if (/[,.\s—\-_]{2,}/.test(a.textContent)) {
            a.textContent = a.textContent.replace(/[,.\s—\-_]+/g, ' ').replace(/\s+/g, ' ').trim();
        }
    });
});
