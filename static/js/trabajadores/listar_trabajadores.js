function cargarTrabajadores() {
    fetch("/api/trabajadores")
        .then(res => res.json())
        .then(data => {
            const cuerpo = document.getElementById("cuerpoTabla");
            cuerpo.innerHTML = "";
            data.forEach(t => {
                cuerpo.innerHTML += `
                    <tr>
                        <td>${t.dni}</td>
                        <td>${t.nombres}</td>
                        <td>${t.apellidos}</td>
                        <td>${t.cargo ?? ""}</td>
                        <td>
                            <button class="btn btn-sm btn-warning" onclick="editarTrabajador(${t.id}, '${t.dni}', '${t.nombres}', '${t.apellidos}', '${t.cargo ?? ""}')">✏️</button>
                            <button class="btn btn-sm btn-danger" onclick="eliminarTrabajador(${t.id})">🗑️</button>
                        </td>
                    </tr>`;
            });
        });
}

cargarTrabajadores();