function verMarcado(tipo, foto, lat, lng) {
    document.getElementById("tituloModalVer").textContent = `Marcado de ${tipo}`;
    document.getElementById("fotoVer").src = foto;

    const contenedorUbicacion = document.getElementById("ubicacionVer");
    if (lat && lng) {
        contenedorUbicacion.innerHTML =
            `<a href="https://www.google.com/maps?q=${lat},${lng}" target="_blank" class="btn btn-outline-primary btn-sm mt-2">📍 Ver en Google Maps</a>`;
    } else {
        contenedorUbicacion.innerHTML = `<p class="text-muted small mt-2">Sin ubicación registrada</p>`;
    }

    const modal = new bootstrap.Modal(document.getElementById("modalVer"));
    modal.show();
}