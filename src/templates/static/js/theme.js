// ==========================
// ダーク / ライトモード切替
// ==========================

// ページロード時にフラッシュが起きないよう即時適用する
(function () {
  if (localStorage.getItem('theme') === 'dark') {
    document.body
      ? document.body.classList.add('dark')
      : document.addEventListener('DOMContentLoaded', () => document.body.classList.add('dark'));
  }
})();

function toggleTheme() {
  const isDark = document.body.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  updateThemeBtn();
}

function updateThemeBtn() {
  const btn = document.getElementById('themeToggle');
  if (!btn) return;
  btn.textContent = document.body.classList.contains('dark') ? 'ライトモード' : 'ダークモード';
}

document.addEventListener('DOMContentLoaded', updateThemeBtn);
