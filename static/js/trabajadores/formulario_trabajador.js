function limpiarFormulario() {
    const form = document.getElementById("formTrabajador");
    const modal = document.getElementById("modalTrabajador");

    if (form) form.reset();
    const idInput = document.getElementById("trabajadorId");
    if (idInput) idInput.value = "";

    const titulo = document.getElementById("tituloFormulario");
    if (titulo) titulo.textContent = "Nuevo Trabajador";

    const btnCancelar = document.getElementById("btnCancelar");
    if (btnCancelar) btnCancelar.classList.add("d-none");

    if (modal) {
        const instance = bootstrap.Modal.getInstance(modal);
        if (instance) instance.hide();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const dniInput = document.getElementById("dni");
    if (dniInput) {
        dniInput.addEventListener("input", function () {
            this.value = this.value.replace(/[^0-9]/g, "").slice(0, 8);
        });
    }

    const form = document.getElementById("formTrabajador");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const id = document.getElementById("trabajadorId").value;
            const dni = document.getElementById("dni").value.trim();

            if (!/^[0-9]{8}$/.test(dni)) {
                mostrarToast("warning", "El DNI debe contener exactamente 8 números");
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
                .then(async res => {
                    const data = await res.json();
                    if (!res.ok) {
                        throw new Error(data.error || "Error al guardar trabajador");
                    }
                    return data;
                })
                .then(data => {
                    limpiarFormulario();
                    cargarTrabajadores();
                    if (typeof cargarInactivos === "function") {
                        cargarInactivos();
                    }
                    mostrarToast("success", data.mensaje || "Trabajador guardado correctamente");
                })
                .catch(err => {
                    mostrarToast("error", err.message);
                });
        });
    }

    const btnCancelar = document.getElementById("btnCancelar");
    if (btnCancelar) {
        btnCancelar.addEventListener("click", limpiarFormulario);
    }

    const btnNuevoTrabajador = document.getElementById("btnNuevoTrabajador");
    if (btnNuevoTrabajador) {
        btnNuevoTrabajador.addEventListener("click", () => {
            const modal = document.getElementById("modalTrabajador");
            const instance = bootstrap.Modal.getOrCreateInstance(modal);
            limpiarFormulario();
            if (modal) {
                const title = document.getElementById("tituloFormulario");
                if (title) title.textContent = "Nuevo Trabajador";
                const btnCancelar = document.getElementById("btnCancelar");
                if (btnCancelar) btnCancelar.classList.add("d-none");
            }
            instance.show();
        });
    }

    const modal = document.getElementById("modalTrabajador");
    if (modal) {
        modal.addEventListener("hidden.bs.modal", () => {
            const form = document.getElementById("formTrabajador");
            if (form) form.reset();
            const idInput = document.getElementById("trabajadorId");
            if (idInput) idInput.value = "";
            const titulo = document.getElementById("tituloFormulario");
            if (titulo) titulo.textContent = "Nuevo Trabajador";
            const btnCancelar = document.getElementById("btnCancelar");
            if (btnCancelar) btnCancelar.classList.add("d-none");
        });
    }
});
