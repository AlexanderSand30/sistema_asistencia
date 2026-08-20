function mostrarTrabajador(data) {
    document.getElementById("infoTrabajadorId").value = data.id;
    document.getElementById("infoDni").value = data.dni;
    document.getElementById("infoNombres").value = data.nombres;
    document.getElementById("infoApellidos").value = data.apellidos;
    document.getElementById("infoCargo").value = data.cargo ?? "";
    document.getElementById("infoObra").value = "";
    document.getElementById("datosTrabajador").classList.remove("d-none");
}

function buscarTrabajadorPorDni() {
    const dni = document.getElementById("dniBuscar").value.trim();

    if (!dni) {
        alert("Ingrese un DNI");
        return;
    }

    fetch(`/api/asistencias/buscar/${dni}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
                document.getElementById("datosTrabajador").classList.add("d-none");
                return;
            }

            mostrarTrabajador(data);
        })
        .catch(err => console.error("Error al buscar:", err));
}

document.getElementById("btnBuscar")?.addEventListener("click", buscarTrabajadorPorDni);

document.getElementById("btnHabilitarBusqueda")?.addEventListener("click", function () {
    document.getElementById("busquedaTrabajador").classList.remove("d-none");
    document.getElementById("contenedorBotonBuscar").classList.remove("d-none");
    this.classList.add("d-none");
});

fetch("/api/asistencias/mi-trabajador")
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        mostrarTrabajador(data);
    })
    .catch(() => alert("No se pudo cargar el trabajador vinculado."));