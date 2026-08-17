const estadoTrabajadores = {
    page: 1,
    perPage: 8,
    totalPages: 1,
    total: 0,
};

function escapeHtml(value = "") {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function renderPaginacionTrabajadores() {
    const contenedor = document.getElementById("paginationTrabajadores");
    if (!contenedor) return;

    if (estadoTrabajadores.totalPages <= 1) {
        contenedor.innerHTML = "";
        return;
    }

    const paginas = [];
    for (let i = 1; i <= estadoTrabajadores.totalPages; i++) {
        paginas.push(i);
    }

    const anterior = Math.max(1, estadoTrabajadores.page - 1);
    const siguiente = Math.min(estadoTrabajadores.totalPages, estadoTrabajadores.page + 1);

    contenedor.innerHTML = `
        <li class="page-item ${estadoTrabajadores.page === 1 ? 'disabled' : ''}">
            <button class="page-link" type="button" data-page="${anterior}" aria-label="Anterior">«</button>
        </li>
        ${paginas.map(p => `
            <li class="page-item ${p === estadoTrabajadores.page ? 'active' : ''}">
                <button class="page-link" type="button" data-page="${p}">${p}</button>
            </li>
        `).join('')}
        <li class="page-item ${estadoTrabajadores.page >= estadoTrabajadores.totalPages ? 'disabled' : ''}">
            <button class="page-link" type="button" data-page="${siguiente}" aria-label="Siguiente">»</button>
        </li>
    `;

    contenedor.querySelectorAll(".page-link").forEach(btn => {
        btn.addEventListener("click", () => {
            const pagina = Number(btn.dataset.page);
            if (pagina && pagina !== estadoTrabajadores.page) {
                cargarTrabajadores(pagina);
            }
        });
    });
}

function cargarTrabajadores(pagina = 1) {
    const cuerpo = document.getElementById("cuerpoTabla");
    const resumen = document.getElementById("resumenTrabajadores");

    if (!cuerpo) return;

    estadoTrabajadores.page = pagina;
    cuerpo.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">Cargando trabajadores...</td></tr>';

    fetch(`/api/trabajadores?page=${pagina}&per_page=${estadoTrabajadores.perPage}`)
        .then(async res => {
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error || "No se pudo cargar la información");
            }
            return data;
        })
        .then(data => {
            const trabajadores = Array.isArray(data.items) ? data.items : [];
            estadoTrabajadores.total      = Number(data.total || 0);
            estadoTrabajadores.totalPages = Number(data.total_pages || 1);
            estadoTrabajadores.page       = Number(data.page || pagina);
            estadoTrabajadores.perPage    = Number(data.per_page || estadoTrabajadores.perPage);

            cuerpo.innerHTML = "";

            if (trabajadores.length === 0) {
                cuerpo.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">No hay trabajadores activos.</td></tr>';
                if (resumen) resumen.textContent = "0 trabajadores registrados";
                renderPaginacionTrabajadores();
                return;
            }

            trabajadores.forEach(t => {
                const cargo = escapeHtml(t.cargo || "-");
                const nombres = escapeHtml(t.nombres || "");
                const apellidos = escapeHtml(t.apellidos || "");
                cuerpo.innerHTML += `
                    <tr>
                        <td>${escapeHtml(t.dni || "")}</td>
                        <td>${nombres}</td>
                        <td>${apellidos}</td>
                        <td>${cargo}</td>
                        <td class="text-center">
                            <button class="btn btn-sm btn-warning me-1" type="button" onclick="editarTrabajador(${t.id}, '${escapeHtml(t.dni || "")}', '${nombres.replace(/'/g, "&#039;")}', '${apellidos.replace(/'/g, "&#039;")}', '${cargo.replace(/'/g, "&#039;")}')" title="Editar trabajador">✏️</button>
                            <button class="btn btn-sm btn-danger" type="button" onclick="eliminarTrabajador(${t.id})" title="Eliminar trabajador">🗑️</button>
                        </td>
                    </tr>`;
            });

            if (resumen) {
                const inicio = (estadoTrabajadores.page - 1) * estadoTrabajadores.perPage + 1;
                const fin = Math.min(inicio + trabajadores.length - 1, estadoTrabajadores.total);
                resumen.textContent = `Mostrando ${inicio}-${fin} de ${estadoTrabajadores.total} trabajadores`;
            }

            renderPaginacionTrabajadores();
        })
        .catch(err => {
            cuerpo.innerHTML = `<tr><td colspan="5" class="text-center text-danger py-4">${escapeHtml(err.message)}</td></tr>`;
            if (resumen) resumen.textContent = "Error al cargar trabajadores";
        });
}

document.addEventListener("DOMContentLoaded", () => {
    const buscar = document.getElementById("buscarTrabajador");
    if (buscar) {
        buscar.addEventListener("input", () => {
            const texto = buscar.value.trim().toLowerCase();
            const filas = [...document.querySelectorAll("#cuerpoTabla tr")];
            filas.forEach(fila => {
                if (!fila.dataset.originalHtml) {
                    fila.dataset.originalHtml = fila.innerHTML;
                }
                const textoFila = fila.textContent.toLowerCase();
                const visible = !texto || textoFila.includes(texto);
                fila.style.display = visible ? "" : "none";
            });
        });
    }

    cargarTrabajadores();
});