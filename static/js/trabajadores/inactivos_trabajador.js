function cargarInactivos() {
    fetch("/api/trabajadores/inactivos?page=1&per_page=10")
        .then(async res => {
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error || "No se pudieron cargar los trabajadores inactivos");
            }
            return data;
        })
        .then(data => {
            const cuerpo = document.getElementById("cuerpoTablaInactivos");
            if (!cuerpo) return;

            const trabajadores = Array.isArray(data.items) ? data.items : [];
            cuerpo.innerHTML = "";

            if (trabajadores.length === 0) {
                cuerpo.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-3">No hay trabajadores inactivos</td></tr>`;
                return;
            }

            trabajadores.forEach(t => {
                cuerpo.innerHTML += `
                    <tr>
                        <td>${t.dni}</td>
                        <td>${t.nombres}</td>
                        <td>${t.apellidos}</td>
                        <td>${t.cargo ?? ""}</td>
                        <td class="text-center">
                            <button class="btn btn-sm btn-success" type="button" onclick="reactivarTrabajador(${t.id})">♻️ Reactivar</button>
                        </td>
                    </tr>`;
            });
        })
        .catch(err => {
            const cuerpo = document.getElementById("cuerpoTablaInactivos");
            if (cuerpo) {
                cuerpo.innerHTML = `<tr><td colspan="5" class="text-center text-danger py-3">${err.message}</td></tr>`;
            }
        });
}

async function reactivarTrabajador(id) {
    if (!await confirmarAccion("El trabajador volverá a estar activo.", "Reactivar")) return;
    fetch(`/api/trabajadores/${id}/reactivar`, { method: "PUT" })
        .then(async res => {
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error || "No se pudo reactivar al trabajador");
            }
            return data;
        })
        .then(data => {
            cargarInactivos();
            cargarTrabajadores();
            mostrarToast("success", data.mensaje || "Trabajador reactivado correctamente");
        })
        .catch(err => {
            mostrarToast("error", err.message);
        });
}