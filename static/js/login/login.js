document.getElementById("formLogin").addEventListener("submit", function (e) {
    e.preventDefault();

    const usuario  = document.getElementById("usuario").value.trim();
    const password = document.getElementById("password").value;
    const mensajeError = document.getElementById("mensajeError");

    mensajeError.classList.add("d-none");

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, password })
    })
    .then(res => res.json().then(data => ({ status: res.status, data })))
    .then(({ status, data }) => {
        if (status !== 200) {
            mensajeError.textContent = data.error;
            mensajeError.classList.remove("d-none");
            return;
        }
        window.location.href = "/";
    })
    .catch(err => {
        mensajeError.textContent = "Error de conexión con el servidor";
        mensajeError.classList.remove("d-none");
        console.error(err);
    });
});