window.mostrarToast = function (icono, mensaje) {
    return Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true
    }).fire({ icon: icono, title: mensaje });
};

window.confirmarAccion = function (mensaje, textoConfirmar = "Confirmar") {
    return Swal.fire({
        icon: "warning",
        title: "¿Estás seguro?",
        text: mensaje,
        showCancelButton: true,
        confirmButtonText: textoConfirmar,
        cancelButtonText: "Cancelar",
        reverseButtons: true
    }).then(resultado => resultado.isConfirmed);
};

const flashMessages = document.getElementById("flashMessages");
if (flashMessages) {
    const toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true
    });

    JSON.parse(flashMessages.dataset.messages).forEach(([categoria, mensaje]) => {
        toast.fire({
            icon: categoria === "danger" ? "error" : categoria,
            title: mensaje
        });
    });
}
