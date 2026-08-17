document.getElementById("dni").addEventListener("input", function () {
    this.value = this.value.replace(/[^0-9]/g, "").slice(0, 8);
});

function limpiarFormulario() {
    document.getElementById("formTrabajador").reset();
    document.getElementById("trabajadorId").value = "";
    document.getElementById("tituloFormulario").textContent = "Nuevo Trabajador";
    document.getElementById("btnCancelar").classList.add("d-none");
}

document.getElementById("formTrabajador").addEventListener("submit", function (e) {
    e.preventDefault();

    const id = document.getElementById("trabajadorId").value;
    const dni = document.getElementById("dni").value.trim();

    if (!/^[0-9]{8}$/.test(dni)) {
        alert("El DNI debe contener exactamente 8 números");
        return;
    }

    const datos = {
        dni: dni,
        nombres: document.getElementById("nombres").value.trim(),
        apellidos: document.getElementById("apellidos").value.trim(),
        cargo: document.getElementById("cargo").value.trim()
    };
    const url = id ? `/api/trabajadores/${id}` : "/api/trabajadores";
    const metodo = id ? "PUT" : "POST";

    fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) { alert("Error: " + data.error); return; }
        limpiarFormulario();
        cargarTrabajadores();
    });
});

document.getElementById("btnCancelar").addEventListener("click", limpiarFormulario);
