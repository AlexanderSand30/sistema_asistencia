function editarTrabajador(id) {
    const modalEl = document.getElementById("modalTrabajador");
    if (!modalEl) return;

    fetch(`/api/trabajadores/${id}`)
        .then(async res => {
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error || "No se pudo cargar la información");
            }
            return data;
        })
        .then(data => {
            const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
            document.getElementById("trabajadorId").value = data.id;
            document.getElementById("dni").value = data.dni;
            document.getElementById("nombres").value = data.nombres;
            document.getElementById("apellidos").value = data.apellidos;
            document.getElementById("cargo").value = data.cargo;
            document.getElementById("f_nac").value = data.fecha_nac || "";
            document.getElementById("f_ini").value = data.fecha_ingreso || "";
            document.getElementById("f_cese").value = data.fecha_cese || "";
            document.getElementById("tituloFormulario").textContent = "Editar Trabajador";
            document.getElementById("btnCancelar").classList.remove("d-none");
            modal.show();
        })
        .catch(err => {
            mostrarToast("error", err.message);
        });


}