// ==UserScript==
// @name         Add loader to all slivmilana pages
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Добавляет лоадер на все 2500 страниц одним кликом
// @author       You
// @match        https://github.com/anykord/slivmilana/edit/main/pages/*
// @grant        none
// ==/UserScript==

const BLOCK = `
<div style="max-width: 680px; margin: 40px auto; text-align: center; font-family: Arial, sans-serif;">
  <div style="position: relative; display: inline-block;">
    <img src="/loading-forever.jpg" alt="Загрузка..." style="width: 100%; max-width: 600px; border-radius: 16px; filter: blur(28px);">
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.88); color: white; padding: 24px 32px; border-radius: 16px; min-width: 320px;">
      <div style="font-size: 20px; margin-bottom: 12px;">Загрузка эксклюзивного фото...</div>
      <div style="font-size: 36px; font-weight: bold; color: #ff5555;" id="timer">30</div>
      <div style="margin-top: 16px; font-size: 18px; line-height: 1.4;">
        Если фото не загрузилось через 30 секунд —<br><b>оно не доступно на сайте.</b><br>
        Перейдите в телеграм-канал чтобы посмотреть его!
      </div>
    </div>
  </div>
  <div style="margin-top: 30px;">
    <a href="https://t.me/+6FpSw688td1hODQy" target="_blank" 
       style="display: inline-block; background: #0088cc; color: white; padding: 18px 48px; font-size: 22px; border-radius: 12px; text-decoration: none; font-weight: bold;">
      Перейти в Telegram-канал (бесплатно, 18+)
    </a>
  </div>
</div>

<script>
let seconds = 30;
const timerElement = document.getElementById('timer');
const interval = setInterval(() => {
  seconds--;
  timerElement.textContent = seconds;
  if (seconds <= 0) clearInterval(interval);
}, 1000);
</script>
`;

// Это запустится автоматически на каждой странице в папке pages
if (document.body && document.querySelector('textarea')) {
  const textarea = document.querySelector('textarea');
  const content = textarea.value;
  if (!content.includes('loading-forever.jpg')) {
    textarea.value = content.replace('</body>', BLOCK + '\n</body>');
    console.log('Лоадер добавлен!');
  }
}