function formatoFecha(date) {
    return date.toLocaleDateString("en-CA"); // YYYY-MM-DD
}

document.getElementById("btnSemanaActual").addEventListener("click", function () {
    const hoy = new Date();
    const diaSemana = hoy.getDay(); // domingo=0, lunes=1...
    const diff = diaSemana === 0 ? -6 : 1 - diaSemana;

    const lunes = new Date(hoy);
    lunes.setDate(hoy.getDate() + diff);

    const sabado = new Date(lunes);
    sabado.setDate(lunes.getDate() + 5);

    document.getElementById("fechaInicio").value = formatoFecha(lunes);
    document.getElementById("fechaFin").value = formatoFecha(sabado);
});

document.getElementById("btnBuscarProduccion").addEventListener("click", function () {
    const inicio = document.getElementById("fechaInicio").value;
    const fin = document.getElementById("fechaFin").value;
    const dni = document.getElementById("dniProduccion").value.trim();
    const cuerpo = document.getElementById("cuerpoTablaProduccion");

    if (!inicio || !fin) {
        mostrarToast("warning", "Selecciona la fecha de inicio y fecha fin");
        return;
    }

    let url = `/api/produccion?inicio=${inicio}&fin=${fin}`;
    if (dni) url += `&dni=${dni}`;

    cuerpo.innerHTML = `<tr><td colspan="7" class="text-center text-muted">Cargando...</td></tr>`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                cuerpo.innerHTML = `<tr><td colspan="7" class="text-center text-danger">${data.error}</td></tr>`;
                return;
            }
            if (data.length === 0) {
                cuerpo.innerHTML = `<tr><td colspan="7" class="text-center text-muted">Sin trabajadores para mostrar</td></tr>`;
                return;
            }

            cuerpo.innerHTML = "";
            data.forEach(p => {
                const horasExtraTexto = p.horas_extra > 0
                    ? `<span class="badge bg-warning text-dark">${p.horas_extra} h</span>`
                    : `0`;
                const faltasTexto = p.faltas > 0
                    ? `<span class="badge bg-danger">${p.faltas}</span>`
                    : `0`;

                cuerpo.innerHTML += `
                    <tr>
                        <td>${p.dni}</td>
                        <td>${p.nombres} ${p.apellidos}</td>
                        <td>${p.cargo ?? ""}</td>
                        <td>${p.horas_trabajadas} h</td>
                        <td>${horasExtraTexto}</td>
                        <td>${faltasTexto}</td>
                    </tr>`;
            });
        })
        .catch(err => {
            cuerpo.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al cargar los datos</td></tr>`;
            console.error(err);
        });
});