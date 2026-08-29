document.getElementById("btnBuscarReporte").addEventListener("click", function () {
    const inicio = document.getElementById("fechaInicio").value;
    const fin = document.getElementById("fechaFin").value;
    const dni = document.getElementById("dniReporte").value.trim();
    const cuerpo = document.getElementById("cuerpoTablaReporte");
    const totalResultados = document.getElementById("totalResultados");
    const btnExportarPDF = document.getElementById("btnExportarPDF");
    const btnExportarExcel = document.getElementById("btnExportarExcel");

    if (!inicio || !fin) {
        mostrarToast("warning", "Selecciona la fecha de inicio y fecha fin");
        return;
    }

    let url = `/api/reportes?inicio=${inicio}&fin=${fin}`;
    if (dni) url += `&dni=${dni}`;

    cuerpo.innerHTML = `<tr><td colspan="9" class="text-center text-muted">Cargando...</td></tr>`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                cuerpo.innerHTML = `<tr><td colspan="9" class="text-center text-danger">${data.error}</td></tr>`;
                totalResultados.textContent = "";
                btnExportarPDF.disabled = true;
                btnExportarExcel.disabled = true;
                return;
            }

            if (data.length === 0) {
                cuerpo.innerHTML = `<tr><td colspan="9" class="text-center text-muted">Sin registros en este rango</td></tr>`;
                totalResultados.textContent = "";
                btnExportarPDF.disabled = true;
                btnExportarExcel.disabled = true;
                return;
            }

            cuerpo.innerHTML = "";
            data.forEach(r => {
                cuerpo.innerHTML += `
                    <tr>
                        <td>${r.dni}</td>
                        <td>${r.nombres}</td>
                        <td>${r.apellidos}</td>
                        <td>${r.obra ?? ""}</td>
                        <td>${r.cargo ?? ""}</td>
                        <td>${r.fecha}</td>
                        <td>${r.hora_entrada}</td>
                        <td>${r.hora_salida}</td>
                        <td>${r.estado}</td>
                    </tr>`;
            });

            totalResultados.textContent = `${data.length} registro(s) encontrado(s)`;
            btnExportarPDF.disabled = false;
            btnExportarExcel.disabled = false;
        })
        .catch(err => {
            cuerpo.innerHTML = `<tr><td colspan="9" class="text-center text-danger">Error al cargar los datos</td></tr>`;
            btnExportarPDF.disabled = true;
            console.error(err);
        });
});

document.getElementById("btnLimpiarFiltros").addEventListener("click", function () {
    // Limpiar filtros
    document.getElementById("fechaInicio").value = "";
    document.getElementById("fechaFin").value = "";
    document.getElementById("dniReporte").value = "";

    // Limpiar resultados
    document.getElementById("cuerpoTablaReporte").innerHTML = `
        <tr id="filaEstadoInicial">
            <td colspan="9" class="text-center text-muted py-4">
                Elige un rango de fechas y haz clic en «Buscar»
            </td>
        </tr>
    `;

    // Limpiar contador
    document.getElementById("totalResultados").textContent = "";

    // Deshabilitar botones de exportación
    document.getElementById("btnExportarPDF").disabled = true;
    document.getElementById("btnExportarExcel").disabled = true;
})