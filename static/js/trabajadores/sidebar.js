document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const closeBtn = document.getElementById('sidebarToggle');
    const openBtn = document.getElementById('sidebarOpenBtn');

    if (!sidebar || !closeBtn || !openBtn) return;

    closeBtn.addEventListener('click', function () {
        sidebar.classList.add('sidebar-hidden');
        openBtn.classList.add('show');
    });

    openBtn.addEventListener('click', function () {
        sidebar.classList.remove('sidebar-hidden');
        openBtn.classList.remove('show');
    });
});
