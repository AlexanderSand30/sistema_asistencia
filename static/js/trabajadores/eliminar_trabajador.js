function eliminarTrabajador(id) {
    if (!confirm("¿Eliminar este trabajador?")) return;
    fetch(`/api/trabajadores/${id}`, { method: "DELETE" })
        .then(async res => {
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error || "No se pudo eliminar al trabajador");
            }
            return data;
        })
        .then(() => {
            cargarTrabajadores();
            if (typeof cargarInactivos === "function") {
                cargarInactivos();
            }
        })
        .catch(err => {
            alert(err.message);
        });
}