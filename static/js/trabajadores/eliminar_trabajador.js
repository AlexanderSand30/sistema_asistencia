function eliminarTrabajador(id) {
    if (!confirm("¿Eliminar este trabajador?")) return;
    fetch(`/api/trabajadores/${id}`, { method: "DELETE" })
        .then(res => res.json())
        .then(() => cargarTrabajadores());
}