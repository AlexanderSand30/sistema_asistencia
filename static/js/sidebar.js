document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebarToggle");
    const openBtn = document.getElementById("sidebarOpenBtn");
    const overlay = document.getElementById("sidebarOverlay");

    if (!sidebar || !toggleBtn || !openBtn) return;


    function cerrarSidebar() {
        sidebar.classList.add("sidebar-hidden");
        openBtn.classList.add("show");
        openBtn.setAttribute("aria-expanded", "false");

        if (overlay) {
            overlay.classList.remove("show");
        }
    }


    function abrirSidebar() {
        sidebar.classList.remove("sidebar-hidden");
        openBtn.classList.remove("show");
        openBtn.setAttribute("aria-expanded", "true");

        if (overlay) {
            overlay.classList.add("show");
        }
    }


    // Botón superior
    toggleBtn.addEventListener("click", function () {
        if (sidebar.classList.contains("sidebar-hidden")) {
            abrirSidebar();
        } else {
            cerrarSidebar();
        }
    });


    // Botón móvil
    openBtn.addEventListener("click", function (event) {
        event.stopPropagation();
        abrirSidebar();
    });


    // Overlay
    if (overlay) {
        overlay.addEventListener("click", function () {
            cerrarSidebar();
        });

    }


    // Cerrar al seleccionar una opción en móvil
    document.querySelectorAll(".sidebar-nav .nav-link").forEach(function (link) {
        link.addEventListener("click", function () {
            if (window.innerWidth <= 767) {
                cerrarSidebar();
            }
        });
    });


    function sincronizarResponsive() {
        const esMovil = window.matchMedia("(max-width: 767.98px)").matches;

        if (esMovil) {
            cerrarSidebar();
            return;
        }

        sidebar.classList.remove("sidebar-hidden");
        openBtn.classList.remove("show");
        openBtn.setAttribute("aria-expanded", "false");
        if (overlay) {
            overlay.classList.remove("show");
        }
    }

    sincronizarResponsive();
    window.addEventListener("resize", sincronizarResponsive);
});
