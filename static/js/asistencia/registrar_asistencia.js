document.getElementById("btnRegistrar").addEventListener("click", function () {
    const trabajador_id = document.getElementById("infoTrabajadorId").value;
    const obra = document.getElementById("infoObra").value.trim();

    if (!obra) {
        mostrarToast("warning", "Ingrese el nombre de la obra");
        return;
    }

    fetch("/api/asistencias", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ trabajador_id, obra })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) { mostrarToast("error", data.error); return; }
        mostrarToast("success", "Asistencia registrada");
        const modal = document.getElementById("modalRegistrarAsistencia");
        bootstrap.Modal.getOrCreateInstance(modal).hide();
        cargarAsistencias();
    })
    .catch(err => console.error("Error al registrar:", err));
});