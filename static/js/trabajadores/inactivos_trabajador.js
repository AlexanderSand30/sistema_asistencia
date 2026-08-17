function cargarInactivos() {
    fetch("/api/trabajadores/inactivos")
        .then(res => res.json())
        .then(data => {
            const cuerpo = document.getElementById("cuerpoTablaInactivos");
            cuerpo.innerHTML = "";

            if (data.length === 0) {
                cuerpo.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No hay trabajadores inactivos</td></tr>`;
                return;
            }

            data.forEach(t => {
                cuerpo.innerHTML += `
                    <tr>
                        <td>${t.dni}</td>
                        <td>${t.nombres}</td>
                        <td>${t.apellidos}</td>
                        <td>${t.cargo ?? ""}</td>
                        <td>
                            <button class="btn btn-sm btn-success" onclick="reactivarTrabajador(${t.id})">♻️ Reactivar</button>
                        </td>
                    </tr>`;
            });
        });
}

function reactivarTrabajador(id) {
    if (!confirm("¿Reactivar este trabajador?")) return;
    fetch(`/api/trabajadores/${id}/reactivar`, { method: "PUT" })
        .then(res => res.json())
        .then(() => {
            cargarInactivos();
            cargarTrabajadores();
        });
}