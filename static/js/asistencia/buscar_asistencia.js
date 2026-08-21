function mostrarTrabajador(data) {
    document.getElementById("infoTrabajadorId").value = data.id;
    document.getElementById("infoDni").value = data.dni;
    document.getElementById("infoNombres").value = data.nombres;
    document.getElementById("infoApellidos").value = data.apellidos;
    document.getElementById("infoCargo").value = data.cargo ?? "";
    document.getElementById("infoObra").value = "";
    document.getElementById("datosTrabajador").classList.remove("d-none");
}

function limpiarFormularioAsistencia() {
    ["infoTrabajadorId", "infoDni", "infoNombres", "infoApellidos", "infoCargo", "infoObra", "dniBuscar"]
        .forEach(id => {
            const campo = document.getElementById(id);
            if (campo) campo.value = "";
        });
    document.getElementById("datosTrabajador")?.classList.add("d-none");
    document.getElementById("busquedaTrabajador")?.classList.add("d-none");
    document.getElementById("contenedorBotonBuscar")?.classList.add("d-none");
    document.getElementById("btnHabilitarBusqueda")?.classList.remove("d-none");
}

function cargarTrabajadorDeSesion() {
    fetch("/api/asistencias/mi-trabajador")
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                mostrarToast("error", data.error);
                const esAdministrador = modalRegistrarAsistencia?.dataset.puedeBuscar === "1";
                if (esAdministrador) {
                    document.getElementById("busquedaTrabajador")?.classList.remove("d-none");
                    document.getElementById("contenedorBotonBuscar")?.classList.remove("d-none");
                }
                return;
            }
            mostrarTrabajador(data);
        })
        .catch(() => mostrarToast("error", "No se pudo cargar el trabajador vinculado."));
}

function buscarTrabajadorPorDni() {
    const dni = document.getElementById("dniBuscar").value.trim();

    if (!dni) {
        mostrarToast("warning", "Ingrese un DNI");
        return;
    }

    fetch(`/api/asistencias/buscar/${dni}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                mostrarToast("error", data.error);
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

const modalRegistrarAsistencia = document.getElementById("modalRegistrarAsistencia");
modalRegistrarAsistencia?.addEventListener("show.bs.modal", limpiarFormularioAsistencia);
modalRegistrarAsistencia?.addEventListener("shown.bs.modal", cargarTrabajadorDeSesion);
modalRegistrarAsistencia?.addEventListener("hidden.bs.modal", limpiarFormularioAsistencia);