function editarTrabajador(id, dni, nombres, apellidos, cargo) {
    const modalEl = document.getElementById("modalTrabajador");
    if (!modalEl) return;

    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    document.getElementById("trabajadorId").value = id;
    document.getElementById("dni").value = dni;
    document.getElementById("nombres").value = nombres;
    document.getElementById("apellidos").value = apellidos;
    document.getElementById("cargo").value = cargo;
    document.getElementById("tituloFormulario").textContent = "Editar Trabajador";
    document.getElementById("btnCancelar").classList.remove("d-none");
    modal.show();
}