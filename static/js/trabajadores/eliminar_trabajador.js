async function eliminarTrabajador(id) {
    if (!await confirmarAccion("El trabajador quedará inactivo.", "Desactivar")) return;
    fetch(`/api/trabajadores/${id}`, { method: "DELETE" })
        .then(async res => {
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error || "No se pudo eliminar al trabajador");
            }
            return data;
        })
        .then(data => {
            cargarTrabajadores();
            if (typeof cargarInactivos === "function") {
                cargarInactivos();
            }
            mostrarToast("success", data.mensaje || "Trabajador desactivado correctamente");
        })
        .catch(err => {
            mostrarToast("error", err.message);
        });
}