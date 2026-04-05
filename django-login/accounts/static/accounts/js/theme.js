document.addEventListener('DOMContentLoaded', function() {
    const root = document.documentElement;
    const toggle = document.getElementById('themeToggle');

    if (!toggle) return;

    const saved = localStorage.getItem('theme') || 'light';

    if (saved === 'dark') {
        root.setAttribute('data-theme', 'dark');
        toggle.checked = true;
    }

    toggle.addEventListener('change', function() {
        const isDark = this.checked;
        root.setAttribute('data-theme', isDark ? 'dark' : 'light');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});