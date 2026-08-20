function construirUrlExportProduccion(base) {
    const inicio = document.getElementById("fechaInicio").value;
    const fin = document.getElementById("fechaFin").value;
    const dni = document.getElementById("dniProduccion").value.trim();

    if (!inicio || !fin) {
        mostrarToast("warning", "Selecciona la fecha de inicio y fecha fin");
        return null;
    }

    let url = `${base}?inicio=${inicio}&fin=${fin}`;
    if (dni) url += `&dni=${dni}`;
    return url;
}

document.getElementById("btnExportarPDF").addEventListener("click", function () {
    const url = construirUrlExportProduccion("/produccion/pdf");
    if (url) window.open(url, "_blank");
});

document.getElementById("btnExportarExcel").addEventListener("click", function () {
    const url = construirUrlExportProduccion("/produccion/excel");
    if (url) window.open(url, "_blank");
});