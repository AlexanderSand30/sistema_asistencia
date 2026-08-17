document.getElementById("btnRegistrar").addEventListener("click", function () {
    const trabajador_id = document.getElementById("infoTrabajadorId").value;
    const obra = document.getElementById("infoObra").value.trim();

    if (!obra) {
        alert("Ingrese el nombre de la obra");
        return;
    }

    fetch("/api/asistencias", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ trabajador_id, obra })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) { alert("Error: " + data.error); return; }
        alert("✅ Asistencia registrada");
        document.getElementById("datosTrabajador").classList.add("d-none");
        document.getElementById("dniBuscar").value = "";
        cargarAsistencias();
    })
    .catch(err => console.error("Error al registrar:", err));
});