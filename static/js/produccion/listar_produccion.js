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
    cargarProduccion();
});

function actualizarResumenProduccion(registros) {
    const horasTrabajadas = registros.reduce((total, registro) => total + Number(registro.horas_trabajadas || 0), 0);
    const horasExtra = registros.reduce((total, registro) => total + Number(registro.horas_extra || 0), 0);
    const faltas = registros.reduce((total, registro) => total + Number(registro.faltas || 0), 0);

    document.getElementById("totalHorasTrabajadas").textContent = `${horasTrabajadas.toFixed(2)} h`;
    document.getElementById("totalHorasExtra").textContent = `${horasExtra.toFixed(2)} h`;
    document.getElementById("totalFaltas").textContent = faltas;
}

function limpiarResumenProduccion() {
    document.getElementById("totalHorasTrabajadas").textContent = "0.00 h";
    document.getElementById("totalHorasExtra").textContent = "0.00 h";
    document.getElementById("totalFaltas").textContent = "0";
}

function cargarProduccion() {
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
                limpiarResumenProduccion();
                cuerpo.innerHTML = `<tr><td colspan="7" class="text-center text-danger">${data.error}</td></tr>`;
                return;
            }
            if (data.length === 0) {
                limpiarResumenProduccion();
                cuerpo.innerHTML = `<tr><td colspan="7" class="text-center text-muted">Sin trabajadores para mostrar</td></tr>`;
                return;
            }

            actualizarResumenProduccion(data);
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
            limpiarResumenProduccion();
            cuerpo.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al cargar los datos</td></tr>`;
            console.error(err);
        });
}

document.getElementById("btnBuscarProduccion").addEventListener("click", cargarProduccion);

function inicializarRangoMesActual() {
    const hoy = new Date();
    const inicio = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
    const fin = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0);
    document.getElementById("fechaInicio").value = formatoFecha(inicio);
    document.getElementById("fechaFin").value = formatoFecha(fin);
    cargarProduccion();
}

inicializarRangoMesActual();