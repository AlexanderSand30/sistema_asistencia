const formUsuario = document.getElementById("formUsuario");
const tituloModalUsuario = document.getElementById("tituloModalUsuario");
const passwordUsuario = document.getElementById("passwordUsuario");
const ayudaPassword = document.getElementById("ayudaPassword");
const contenedorEstadoUsuario = document.getElementById("contenedorEstadoUsuario");
const estadoUsuario = document.getElementById("estadoUsuario");
const nroDocumento = document.getElementById("nroDocumentoUsuario");

function prepararNuevoUsuario() {
    formUsuario.reset();
    // formUsuario.action = "{{ url_for('usuario.crear') }}";
    formUsuario.action = "crear";
    tituloModalUsuario.textContent = "Nuevo usuario";
    passwordUsuario.required = true;
    ayudaPassword.textContent = "Mínimo 6 caracteres.";
    contenedorEstadoUsuario.classList.add("d-none");
    nroDocumento.disabled = false;
}

function prepararEditarUsuario(boton) {
    const {
        id,
        nombre,
        usuario,
        nroDocumento,
        rol,
        estado
    } = boton.dataset;
    formUsuario.reset();
    formUsuario.action = `/usuarios/editar/${id}`;
    tituloModalUsuario.textContent = "Editar usuario";
    document.getElementById("nombreUsuario").value = nombre;
    document.getElementById("nroDocumentoUsuario").value = nroDocumento || "";
    document.getElementById("loginUsuario").value = usuario;
    document.getElementById("rolUsuario").value = rol;
    nroDocumento.disabled = true;
    estadoUsuario.checked = Boolean(estado);
    passwordUsuario.required = false;
    ayudaPassword.textContent = "Déjala vacía para conservar la contraseña actual.";
    contenedorEstadoUsuario.classList.remove("d-none");
}