document.getElementById("btnFiltrar").addEventListener("click", function () {
    const inicio = document.getElementById("filtroFechaInicio").value;
    const fin = document.getElementById("filtroFechaFin").value;

    if (!inicio || !fin) {
        alert("Selecciona ambas fechas para filtrar");
        return;
    }
    cargarAsistencias(inicio, fin, 1);
});

document.getElementById("btnHoy").addEventListener("click", function () {
    const hoy = new Date().toLocaleDateString("en-CA");
    document.getElementById("filtroFechaInicio").value = hoy;
    document.getElementById("filtroFechaFin").value = hoy;
    cargarAsistencias(hoy, hoy, 1);
});

document.getElementById("btnVerTodos").addEventListener("click", function () {
    document.getElementById("filtroFechaInicio").value = "";
    document.getElementById("filtroFechaFin").value = "";
    cargarAsistencias("", "", 1);
});
